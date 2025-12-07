# memory_manager.py
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import json


class MemoryManager:
    def __init__(self, persist_dir="./memory_db", collection_name="assistant_memory"):
        """Инициализация системы памяти"""
        # Векторная модель для эмбеддингов (384 измерения, быстрая)
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        # ChromaDB клиент с постоянным хранением
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

        # Коллекция для хранения памяти
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # косинусное расстояние для поиска
        )

    def add_memory(self, content: str, memory_type: str = "user_info",
                   metadata: Optional[Dict] = None) -> str:
        """
        Добавить новую запись в память

        Args:
            content: Текст для запоминания
            memory_type: Тип памяти (user_info, rule, preference, fact)
            metadata: Дополнительные метаданные

        Returns:
            ID созданной записи
        """
        memory_id = str(uuid.uuid4())

        # Создаём эмбеддинг
        embedding = self.embedder.encode(content).tolist()

        # Формируем метаданные
        mem_metadata = {
            "type": memory_type,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        if metadata:
            mem_metadata.update(metadata)

        # Сохраняем в базу
        self.collection.add(
            ids=[memory_id],
            documents=[content],
            embeddings=[embedding],
            metadatas=[mem_metadata]
        )

        print(f"✅ Память сохранена: {memory_id[:8]}... - {content[:50]}...")
        return memory_id

    def search_memory(self, query: str, top_k: int = 3,
                      memory_type: Optional[str] = None) -> List[Dict]:
        """
        Поиск релевантных воспоминаний

        Args:
            query: Поисковый запрос
            top_k: Количество результатов
            memory_type: Фильтр по типу памяти

        Returns:
            Список найденных воспоминаний
        """
        # Создаём эмбеддинг запроса
        query_embedding = self.embedder.encode(query).tolist()

        # Формируем фильтр
        where_filter = {"type": memory_type} if memory_type else None

        # Поиск
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )

        # Форматируем результаты
        memories = []
        if results['ids']:
            for i, doc_id in enumerate(results['ids'][0]):
                memories.append({
                    "id": doc_id,
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "relevance": 1 - results['distances'][0][i]  # конвертируем расстояние в релевантность
                })

        return memories

    def update_memory(self, memory_id: str, new_content: str,
                      new_metadata: Optional[Dict] = None):
        """
        Обновить существующую запись

        Args:
            memory_id: ID записи для обновления
            new_content: Новый текст
            new_metadata: Новые метаданные
        """
        # Получаем старую запись
        old = self.collection.get(ids=[memory_id])
        if not old['ids']:
            print(f"❌ Память {memory_id} не найдена")
            return

        # Обновляем метаданные
        metadata = old['metadatas'][0]
        metadata['updated_at'] = datetime.now().isoformat()
        if new_metadata:
            metadata.update(new_metadata)

        # Создаём новый эмбеддинг
        embedding = self.embedder.encode(new_content).tolist()

        # Обновляем
        self.collection.update(
            ids=[memory_id],
            documents=[new_content],
            embeddings=[embedding],
            metadatas=[metadata]
        )

        print(f"✅ Память обновлена: {memory_id[:8]}...")

    def delete_memory(self, memory_id: str):
        """Удалить запись из памяти"""
        self.collection.delete(ids=[memory_id])
        print(f"🗑️ Память удалена: {memory_id[:8]}...")

    def list_all_memories(self, memory_type: Optional[str] = None) -> List[Dict]:
        """
        Получить все записи в памяти

        Args:
            memory_type: Фильтр по типу

        Returns:
            Список всех воспоминаний
        """
        where_filter = {"type": memory_type} if memory_type else None

        results = self.collection.get(
            where=where_filter,
            include=["documents", "metadatas"]
        )

        memories = []
        if results['ids']:
            for i, doc_id in enumerate(results['ids']):
                memories.append({
                    "id": doc_id,
                    "content": results['documents'][i],
                    "metadata": results['metadatas'][i]
                })

        return memories

    def clear_all_memories(self):
        """Очистить всю память (осторожно!)"""
        # Удаляем и создаём коллекцию заново
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
        print("🗑️ Вся память очищена")

    def extract_important_info(self, conversation_text: str) -> Optional[str]:
        """
        Извлечь важную информацию из диалога для запоминания
        (можно улучшить с помощью LLM)

        Args:
            conversation_text: Текст диалога

        Returns:
            Важная информация или None
        """
        # Простые ключевые слова для обнаружения важной информации
        important_keywords = [
            "меня зовут", "я работаю", "я люблю", "мой любимый",
            "я предпочитаю", "запомни", "важно", "всегда делай",
            "никогда не", "мне нравится", "я не люблю"
        ]

        text_lower = conversation_text.lower()
        for keyword in important_keywords:
            if keyword in text_lower:
                return conversation_text

        return None
