from typing import Any, List, Dict, Optional
from py_amo.exceptions import ValidationError


def validate_entity_id(entity_id: Any) -> int:
    """Валидация ID сущности"""
    if entity_id is None:
        raise ValidationError("Entity ID cannot be None")
    
    try:
        entity_id_int = int(entity_id)
        if entity_id_int <= 0:
            raise ValidationError("Entity ID must be positive")
        return entity_id_int
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid entity ID: {entity_id}")


def validate_entity_ids(entity_ids: List[Any]) -> List[int]:
    """Валидация списка ID сущностей"""
    if not entity_ids:
        raise ValidationError("Entity IDs list cannot be empty")
    
    validated_ids = []
    for entity_id in entity_ids:
        validated_ids.append(validate_entity_id(entity_id))
    
    return validated_ids


def validate_limit(limit: Any) -> int:
    """Валидация лимита записей"""
    if limit is None:
        return 250  # Значение по умолчанию
    
    try:
        limit_int = int(limit)
        if limit_int <= 0:
            raise ValidationError("Limit must be positive")
        if limit_int > 250:
            raise ValidationError("AmoCRM API limit is 250")
        return limit_int
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid limit: {limit}")


def validate_page(page: Any) -> int:
    """Валидация номера страницы"""
    if page is None:
        return 1  # Значение по умолчанию
    
    try:
        page_int = int(page)
        if page_int <= 0:
            raise ValidationError("Page number must be positive")
        return page_int
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid page number: {page}")


def validate_entity_type(entity_type: str) -> str:
    """Валидация типа сущности"""
    valid_types = [
        "leads", "contacts", "companies", "customers", 
        "tasks", "notes", "events", "catalogs"
    ]
    
    if entity_type not in valid_types:
        raise ValidationError(f"Invalid entity type: {entity_type}. Valid types: {valid_types}")
    
    return entity_type


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Валидация обязательных полей"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        raise ValidationError(f"Missing required fields: {missing_fields}") 