from datetime import datetime, timezone
from typing import Optional, Union


def datetime_to_timestamp(dt: datetime) -> int:
    """Конвертирует datetime в timestamp для AmoCRM API"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def timestamp_to_datetime(timestamp: Union[int, str]) -> Optional[datetime]:
    """Конвертирует timestamp из AmoCRM API в datetime"""
    if timestamp is None:
        return None
    
    try:
        timestamp_int = int(timestamp)
        return datetime.fromtimestamp(timestamp_int, tz=timezone.utc)
    except (ValueError, TypeError):
        return None


def now_timestamp() -> int:
    """Возвращает текущий timestamp"""
    return datetime_to_timestamp(datetime.now(timezone.utc))


def format_date_for_filter(dt: datetime) -> str:
    """Форматирует дату для использования в фильтрах AmoCRM"""
    return str(datetime_to_timestamp(dt)) 