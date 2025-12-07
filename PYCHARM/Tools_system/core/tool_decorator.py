# core/tool_decorator.py
from typing import Callable, Dict, Any, List
import inspect


class ToolRegistry:
    """Реестр всех доступных инструментов"""

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.functions: Dict[str, Callable] = {}

    def register(self, name: str, description: str, parameters: Dict[str, Any]):
        """Декоратор для регистрации инструмента"""

        def decorator(func: Callable):
            # Сохраняем функцию
            self.functions[name] = func

            # Формируем описание в формате Ollama
            self.tools[name] = {
                'type': 'function',
                'function': {
                    'name': name,
                    'description': description,
                    'parameters': parameters
                }
            }
            return func

        return decorator

    def get_tool_definitions(self) -> List[Dict]:
        """Возвращает список инструментов для Ollama"""
        return list(self.tools.values())

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Вызов инструмента по имени"""
        if name not in self.functions:
            return {"error": f"Инструмент {name} не найден"}

        try:
            return self.functions[name](**arguments)
        except Exception as e:
            return {"error": f"Ошибка выполнения {name}: {str(e)}"}


# Глобальный реестр
registry = ToolRegistry()
