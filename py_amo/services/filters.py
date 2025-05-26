from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime
from functools import wraps
from enum import Enum


class FilterOperator(Enum):
    """Операторы для фильтрации"""
    EQUALS = "eq"
    NOT_EQUALS = "ne"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    IN = "in"
    NOT_IN = "not_in"
    LIKE = "like"
    NOT_LIKE = "not_like"


class FilterBuilder:
    """Строитель фильтров для AmoCRM API"""
    
    def __init__(self):
        self.filters: Dict[str, Any] = {}
        self.order: Dict[str, str] = {}
        self.with_fields: List[str] = []
        self.page_params: Dict[str, int] = {}
    
    def add_filter(self, field: str, value: Any, operator: FilterOperator = FilterOperator.EQUALS) -> 'FilterBuilder':
        """Добавить фильтр"""
        if operator == FilterOperator.EQUALS:
            filter_key = f"filter[{field}]"
        else:
            filter_key = f"filter[{field}][{operator.value}]"
        
        if isinstance(value, (list, tuple)):
            self.filters[filter_key] = ",".join(map(str, value))
        elif isinstance(value, datetime):
            self.filters[filter_key] = int(value.timestamp())
        else:
            self.filters[filter_key] = value
        
        return self
    
    def filter_by_id(self, entity_id: Union[int, List[int]]) -> 'FilterBuilder':
        """Фильтр по ID"""
        if isinstance(entity_id, list):
            return self.add_filter("id", entity_id, FilterOperator.IN)
        return self.add_filter("id", entity_id)
    
    def filter_by_responsible(self, user_id: Union[int, List[int]]) -> 'FilterBuilder':
        """Фильтр по ответственному"""
        return self.add_filter("responsible_user_id", user_id)
    
    def filter_by_created_at(self, from_date: datetime = None, to_date: datetime = None) -> 'FilterBuilder':
        """Фильтр по дате создания"""
        if from_date:
            self.add_filter("created_at", from_date, FilterOperator.GREATER_THAN_OR_EQUAL)
        if to_date:
            self.add_filter("created_at", to_date, FilterOperator.LESS_THAN_OR_EQUAL)
        return self
    
    def filter_by_updated_at(self, from_date: datetime = None, to_date: datetime = None) -> 'FilterBuilder':
        """Фильтр по дате обновления"""
        if from_date:
            self.add_filter("updated_at", from_date, FilterOperator.GREATER_THAN_OR_EQUAL)
        if to_date:
            self.add_filter("updated_at", to_date, FilterOperator.LESS_THAN_OR_EQUAL)
        return self
    
    def filter_by_pipeline(self, pipeline_id: Union[int, List[int]]) -> 'FilterBuilder':
        """Фильтр по воронке (для сделок)"""
        return self.add_filter("pipeline_id", pipeline_id)
    
    def filter_by_status(self, status_id: Union[int, List[int]]) -> 'FilterBuilder':
        """Фильтр по статусу"""
        return self.add_filter("status_id", status_id)
    
    def order_by(self, field: str, direction: str = "asc") -> 'FilterBuilder':
        """Добавить сортировку"""
        if direction.lower() not in ["asc", "desc"]:
            raise ValueError("Direction must be 'asc' or 'desc'")
        
        self.order[f"order[{field}]"] = direction.lower()
        return self
    
    def with_field(self, field: str) -> 'FilterBuilder':
        """Добавить поле для включения в ответ"""
        if field not in self.with_fields:
            self.with_fields.append(field)
        return self
    
    def with_contacts(self) -> 'FilterBuilder':
        """Включить контакты в ответ"""
        return self.with_field("contacts")
    
    def with_companies(self) -> 'FilterBuilder':
        """Включить компании в ответ"""
        return self.with_field("companies")
    
    def with_catalog_elements(self) -> 'FilterBuilder':
        """Включить элементы каталогов в ответ"""
        return self.with_field("catalog_elements")
    
    def limit(self, limit: int) -> 'FilterBuilder':
        """Установить лимит записей"""
        if limit <= 0:
            raise ValueError("Limit must be positive")
        if limit > 250:
            raise ValueError("AmoCRM API limit is 250")
        
        self.page_params["limit"] = limit
        return self
    
    def page(self, page_num: int) -> 'FilterBuilder':
        """Установить номер страницы"""
        if page_num <= 0:
            raise ValueError("Page number must be positive")
        
        self.page_params["page"] = page_num
        return self
    
    def build(self) -> Dict[str, Any]:
        """Построить финальный словарь параметров"""
        params = {}
        
        # Добавляем фильтры
        params.update(self.filters)
        
        # Добавляем сортировку
        params.update(self.order)
        
        # Добавляем поля для включения
        if self.with_fields:
            params["with"] = ",".join(self.with_fields)
        
        # Добавляем параметры пагинации
        params.update(self.page_params)
        
        return params


def with_kwargs_filter(func: Callable) -> Callable:
    """Декоратор для автоматической фильтрации kwargs"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Удаляем None значения
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return func(*args, **filtered_kwargs)
    return wrapper


def create_filter() -> FilterBuilder:
    """Создать новый экземпляр FilterBuilder"""
    return FilterBuilder()
