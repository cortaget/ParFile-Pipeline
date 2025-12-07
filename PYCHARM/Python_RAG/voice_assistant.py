# voice_assistant.py
import json
import requests
import pyttsx3
import pyaudio
from vosk import Model, KaldiRecognizer
from core.plugin_loader import load_plugins, run_plugin
import threading
import queue
from memory_manager import MemoryManager  # ✅ НОВОЕ

# 🌐 Настройки Ollama
LLM_URL = "http://127.0.0.1:11434/api/generate"
LLM_MODEL = "gemma3:4b"

# 🧠 Инициализация памяти
memory = MemoryManager()  # ✅ НОВОЕ

# 🎤 Инициализация распознавания речи
model = Model("E:\\python\\PYCHARM\\UZISpeach\\vosk-model-small-ru-0.22")
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4096)
stream.start_stream()

# ✅ Очередь для озвучки + выделенный поток
speech_queue = queue.Queue()


def speech_worker():
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    for voice in voices:
        if "irina" in voice.name.lower():
            tts.setProperty('voice', voice.id)
            print(f"✅ Используется голос: {voice.name}")
            break
    tts.setProperty('rate', 160)

    while True:
        text = speech_queue.get()
        if text is None:
            break
        tts.say(text)
        tts.runAndWait()
        speech_queue.task_done()


speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()


def speak(text):
    speech_queue.put(text)


def listen_command():
    print("🎙️ Говори (на русском)...")
    try:
        stream.read(stream.get_read_available(), exception_on_overflow=False)
    except:
        pass

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                print(f"📝 Распознано: {text}")
                return text


chat_history = []
use_stream = True
MAX_HISTORY = 20


def query_llm_stream(user_input):
    """Запрос к LLM с использованием RAG памяти"""
    chat_history.append(f"User: {user_input}")

    # Поиск релевантных воспоминаний
    relevant_memories = memory.search_memory(user_input, top_k=3)

    # Формируем контекст с памятью
    memory_context = ""
    if relevant_memories:
        memory_context = "\n[Важная информация из памяти]:\n"
        for mem in relevant_memories:
            if mem['relevance'] > 0.5:
                memory_context += f"- {mem['content']}\n"
        memory_context += "\n"

    # Формируем промпт
    context = chat_history[-MAX_HISTORY:]
    full_prompt = memory_context + "\n".join(context) + "\nAssistant:"

    payload = {
        "model": LLM_MODEL,
        "prompt": full_prompt,
        "stream": True
    }

    try:
        response = requests.post(LLM_URL, json=payload, stream=True)

        if response.status_code != 200:
            return f"Ошибка: {response.status_code}"

        reply = ""
        print("💬 Ответ ИИ:", end=' ', flush=True)

        for line in response.iter_lines():
            if line:
                part = json.loads(line.decode('utf-8')).get("response", "")
                print(part, end='', flush=True)
                reply += part

        print()
        chat_history.append(f"Assistant: {reply}")

        # ✅ НОВОЕ: Умное извлечение через LLM
        extracted_facts = memory.extract_with_llm(
            user_input,
            reply,
            LLM_URL,
            LLM_MODEL
        )

        # Сохраняем извлечённые факты
        for fact in extracted_facts:
            memory.add_memory(fact, memory_type="user_info")
            print(f"🧠 Запомнил: {fact}")

        return reply

    except Exception as e:
        return f"Ошибка: {str(e)}"


# ✅ НОВОЕ: Команды управления памятью
def handle_memory_commands(user_input: str) -> bool:
    """Обработка команд памяти"""
    lower_input = user_input.lower()

    # Команда: запомнить
    if "запомни" in lower_input or "сохрани в памяти" in lower_input:
        # Извлекаем текст после команды
        content = user_input.split("запомни", 1)[-1].strip() if "запомни" in lower_input else \
            user_input.split("сохрани в памяти", 1)[-1].strip()

        if content:
            memory.add_memory(content, memory_type="user_info")
            speak("Хорошо, я запомнил это")
            return True

    # Команда: что ты помнишь
    if "что ты помнишь" in lower_input or "покажи память" in lower_input:
        memories = memory.list_all_memories()
        if memories:
            response = f"Я помню {len(memories)} записей:\n"
            for i, mem in enumerate(memories[:5], 1):  # показываем первые 5
                response += f"{i}. {mem['content'][:50]}...\n"
            print(response)
            speak(f"Я помню {len(memories)} записей. Детали в консоли")
        else:
            speak("Моя память пуста")
        return True

    # Команда: очистить память
    if "очисти память" in lower_input or "забудь всё" in lower_input:
        memory.clear_all_memories()
        speak("Память очищена")
        return True

    return False


def main():
    plugin_handlers = load_plugins()

    print("🧠 Локальный голосовой ассистент с RAG памятью")
    speak("Привет, хозяин! Теперь у меня есть память")

    while True:
        user_input = listen_command()
        if not user_input:
            continue

        if any(word in user_input for word in ["выход", "стоп", "выключись", "закройся"]):
            speak("Пока, хозяин!")
            print("👋 Завершение работы.")
            speech_queue.put(None)
            speech_thread.join(timeout=2)
            break

        # ✅ НОВОЕ: Проверяем команды памяти
        if handle_memory_commands(user_input):
            continue

        handled = False
        for handler in plugin_handlers:
            result = handler(user_input)
            if result:
                chat_history.append(f"Assistant: {result}")
                print("🧩 Плагин:", result)
                speak(result)
                handled = True
                break

        if not handled:
            reply = query_llm_stream(user_input)
            speak(reply)


if __name__ == "__main__":
    main()
