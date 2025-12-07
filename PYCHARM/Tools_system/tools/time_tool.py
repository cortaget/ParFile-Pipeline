# tools/time_tool.py
from core.tool_decorator import registry
from datetime import datetime


@registry.register(
    name="get_current_time",
    description="Получает текущее время и дату",
    parameters={
        'type': 'object',
        'properties': {
            'format': {
                'type': 'string',
                'description': 'Формат вывода: time (только время), date (только дата), full (полная дата и время)',
                'enum': ['time', 'date', 'full']
            }
        },
        'required': ['format']
    }
)
def get_current_time(format: str = 'full') -> dict:
    """Возвращает текущее время"""
    now = datetime.now()

    if format == 'time':
        return {"time": now.strftime("%H:%M:%S")}
    elif format == 'date':
        return {"date": now.strftime("%Y-%m-%d")}
    else:
        return {
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": now.strftime("%A")
        }
