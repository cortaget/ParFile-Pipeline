# tools/calculator_tool.py
from core.tool_decorator import registry


@registry.register(
    name="calculate",
    description="Выполняет математические вычисления (сложение, вычитание, умножение, деление)",
    parameters={
        'type': 'object',
        'properties': {
            'expression': {
                'type': 'string',
                'description': 'Математическое выражение для вычисления, например: 2+2 или 10*5'
            }
        },
        'required': ['expression']
    }
)
def calculate(expression: str) -> dict:
    """Безопасный калькулятор"""
    try:
        # Безопасное вычисление только базовых операций
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return {"error": "Недопустимые символы в выражении"}

        result = eval(expression, {"__builtins__": {}}, {})
        return {"result": result, "expression": expression}
    except Exception as e:
        return {"error": f"Ошибка вычисления: {str(e)}"}
