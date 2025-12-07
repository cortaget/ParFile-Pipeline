# voice_assistant.py
import json
import requests
from core.tool_decorator import registry

# Импортируем все инструменты
from tools import calculator_tool, time_tool

# Настройки Ollama
LLM_URL = "http://127.0.0.1:11434/api/chat"
LLM_MODEL = "gemma3:4b"

chat_history = []


def query_llm_with_tools(user_input: str) -> str:
    """Запрос к LLM с поддержкой инструментов"""

    # Добавляем сообщение пользователя
    messages = chat_history + [{"role": "user", "content": user_input}]

    # Получаем список доступных инструментов
    tools = registry.get_tool_definitions()

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "tools": tools,
        "stream": False
    }

    try:
        response = requests.post(LLM_URL, json=payload)

        if response.status_code != 200:
            return f"Ошибка: {response.status_code}"

        result = response.json()
        message = result.get("message", {})

        # Проверяем, хочет ли модель вызвать инструмент
        if "tool_calls" in message and message["tool_calls"]:
            print("🔧 Модель вызывает инструмент...")

            # Обрабатываем вызовы инструментов
            tool_results = []
            for tool_call in message["tool_calls"]:
                function = tool_call.get("function", {})
                tool_name = function.get("name")
                arguments = function.get("arguments", {})

                print(f"   → {tool_name}({arguments})")

                # Вызываем инструмент
                result = registry.call_tool(tool_name, arguments)
                tool_results.append({
                    "role": "tool",
                    "content": json.dumps(result, ensure_ascii=False)
                })

            # Добавляем результаты и запрашиваем финальный ответ
            messages.append(message)
            messages.extend(tool_results)

            # Повторный запрос с результатами инструментов
            payload["messages"] = messages
            payload.pop("tools")  # Убираем tools для финального ответа

            final_response = requests.post(LLM_URL, json=payload)
            final_message = final_response.json().get("message", {})
            final_content = final_message.get("content", "")

            # Сохраняем в историю
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": final_content})

            return final_content
        else:
            # Обычный ответ без инструментов
            content = message.get("content", "")
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": content})
            return content

    except Exception as e:
        return f"Ошибка: {str(e)}"
