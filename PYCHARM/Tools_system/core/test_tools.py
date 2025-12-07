# core/test_tools.py
from core.tool_decorator import registry
from typing import Dict, Any, List
import json


class ToolTester:
    """Система тестирования инструментов"""

    def __init__(self):
        self.test_results = []

    def test_tool(self, tool_name: str, test_cases: List[Dict[str, Any]]) -> None:
        """Тестирование инструмента с набором тест-кейсов"""
        print(f"\n{'=' * 60}")
        print(f"🧪 Тестирование инструмента: {tool_name}")
        print(f"{'=' * 60}")

        if tool_name not in registry.functions:
            print(f"❌ Инструмент {tool_name} не найден!")
            return

        passed = 0
        failed = 0

        for i, test_case in enumerate(test_cases, 1):
            input_args = test_case.get("input", {})
            expected = test_case.get("expected", None)
            description = test_case.get("description", f"Тест {i}")

            print(f"\n📝 {description}")
            print(f"   Входные данные: {json.dumps(input_args, ensure_ascii=False)}")

            # Вызываем инструмент
            result = registry.call_tool(tool_name, input_args)
            print(f"   Результат: {json.dumps(result, ensure_ascii=False)}")

            # Проверяем результат
            if expected is not None:
                if self._compare_results(result, expected):
                    print(f"   ✅ PASSED")
                    passed += 1
                else:
                    print(f"   ❌ FAILED")
                    print(f"   Ожидалось: {json.dumps(expected, ensure_ascii=False)}")
                    failed += 1
            else:
                # Если expected не указан, просто проверяем на ошибки
                if "error" not in result:
                    print(f"   ✅ PASSED (без ошибок)")
                    passed += 1
                else:
                    print(f"   ⚠️  WARNING (есть ошибка)")

        print(f"\n{'=' * 60}")
        print(f"📊 Результаты: ✅ {passed} пройдено | ❌ {failed} провалено")
        print(f"{'=' * 60}\n")

    def _compare_results(self, result: Any, expected: Any) -> bool:
        """Сравнение результатов"""
        if isinstance(expected, dict):
            return all(result.get(k) == v for k, v in expected.items())
        return result == expected

    def test_all_tools(self) -> None:
        """Быстрый тест всех инструментов"""
        print("\n🚀 Быстрая проверка всех инструментов\n")

        for tool_name in registry.functions.keys():
            tool_def = registry.tools[tool_name]['function']
            print(f"✓ {tool_name}: {tool_def['description']}")

        print(f"\nВсего инструментов: {len(registry.functions)}")


# Пример использования
if __name__ == "__main__":
    # Импортируем инструменты
    from tools import calculator_tool, time_tool

    tester = ToolTester()

    # Тест калькулятора
    tester.test_tool("calculate", [
        {
            "description": "Простое сложение",
            "input": {"expression": "2+2"},
            "expected": {"result": 4, "expression": "2+2"}
        },
        {
            "description": "Умножение",
            "input": {"expression": "5*10"},
            "expected": {"result": 50}
        },
        {
            "description": "Сложное выражение",
            "input": {"expression": "(10+5)*2"},
            "expected": {"result": 30}
        },
        {
            "description": "Ошибка: недопустимые символы",
            "input": {"expression": "import os"},
            "expected": None  # Ожидаем ошибку
        }
    ])

    # Тест времени
    tester.test_tool("get_current_time", [
        {
            "description": "Получение только времени",
            "input": {"format": "time"},
            "expected": None  # Результат зависит от текущего времени
        },
        {
            "description": "Получение только даты",
            "input": {"format": "date"},
            "expected": None
        }
    ])

    # Общая проверка
    tester.test_all_tools()
