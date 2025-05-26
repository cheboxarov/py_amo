from typing import TypeVar, Generic, Optional, List, Dict, Any
from py_amo.schemas.entity_link_schema import EntityLinksSchema
from py_amo.schemas.created_entity_schema import CreatedEntity
from py_amo.services.filters import with_kwargs_filter
from py_amo.exceptions import (
    EntityNotFoundError, 
    get_exception_from_status_code,
    UnsupportedOperationError
)
import json
import requests

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session):
        """
        session - AmoSession

        """
        self.session = session.get_requests_session()
        self.base_url = session.get_url() + self.REPOSITORY_PATH
        self.entity_type = self.ENTITY_TYPE
        self.schema_class = self.SCHEMA_CLASS
        self.schema_input_class = self.SCHEMA_INPUT_CLASS
        self.subdomain = session.get_subdomain()

    def get_base_url(self) -> str:
        return self.base_url

    def get_entity_type(self) -> str:
        return self.entity_type

    def _handle_response_error(self, response: requests.Response, operation: str = "API request"):
        """Обработка ошибок HTTP ответов"""
        if response.status_code >= 400:
            try:
                error_data = response.json()
            except (ValueError, json.JSONDecodeError):
                error_data = {"detail": response.text}
            
            message = error_data.get("detail", f"{operation} failed")
            raise get_exception_from_status_code(response.status_code, message, error_data)

    def count(self, **kwargs) -> int:
        """Получить количество сущностей без загрузки самих данных"""
        params = kwargs.copy()
        params["limit"] = 1
        
        response = self.session.get(self.get_base_url(), params=params)
        if response.status_code >= 400:
            self._handle_response_error(response, "Count operation")
        
        data = response.json()
        return data.get("_page", {}).get("total", 0)

    def exists(self, entity_id: int) -> bool:
        """Проверить существование сущности по ID"""
        url = f"{self.get_base_url()}/{entity_id}"
        response = self.session.head(url)
        return response.status_code == 200

    @with_kwargs_filter
    def get_all(self, **kwargs) -> List[T]:
        """
        kwargs:

        - limit: int
        - with_: str (Смотреть в документации)
        - offset: int

        Чтобы узнать остальные параметры - обращайтесь к офф. документации.

        """
        response = self.session.get(self.get_base_url(), params=kwargs)
        if response.status_code >= 400:
            self._handle_response_error(response, "Get all entities")
        
        data = response.json()
        row_entities = data.get("_embedded", {}).get(self.get_entity_type(), [])
        return [self.schema_class(**item) for item in row_entities]

    @with_kwargs_filter
    def get_by_id(self, entity_id: int, **kwargs) -> Optional[T]:
        """
        kwargs:

        - with_: str (Смотреть в документации)

        Чтобы узнать остальные параметры - обращайтесь к офф. документации.

        """

        url = f"{self.get_base_url()}/{entity_id}"
        response = self.session.get(url, params=kwargs)
        if response.status_code in [404, 204]:
            return None
        if response.status_code >= 400:
            self._handle_response_error(response, f"Get {self.entity_type} by id {entity_id}")
        
        return self.schema_class(**response.json())

    def create(self, entities: List[T]) -> List[CreatedEntity]:
        headers = {"Content-Type": "application/json"}
        response = self.session.post(
            self.get_base_url(),
            data=json.dumps([entity.dict(exclude_none=True) for entity in entities]),
            headers=headers
        )
        if response.status_code >= 400:
            self._handle_response_error(response, f"Create {self.entity_type}")
        
        response_data = response.json()
        embedded_key = self.entity_type if self.entity_type != "companies" else "companies"
        created_entities = response_data.get("_embedded", {}).get(embedded_key, [])
        
        created_ids = [
            CreatedEntity(
                id=created_entity.get("id"),
                entity_type=self.entity_type,
                link=created_entity.get("_links", {}).get("self", {}).get("href"),
            )
            for created_entity in created_entities
        ]
        return created_ids

    def update(self, entity: T) -> T:
        entity_data = entity.dict(exclude_none=True)
        entity_id = entity_data.pop("id")
        if entity_id is None:
            raise ValueError("entity needs id for update")
        
        update_data = self.schema_input_class(**entity_data).dict(exclude_none=True)
        response = self.session.patch(
            self.get_base_url() + f"/{entity_id}", json=update_data
        )
        if response.status_code >= 400:
            self._handle_response_error(response, f"Update {self.entity_type} with id {entity_id}")
        
        return self.schema_class(**response.json())

    def delete(self, entity_id: int) -> bool:
        url = f"{self.get_base_url()}/{entity_id}"
        response = self.session.delete(url)
        if response.status_code >= 400:
            self._handle_response_error(response, f"Delete {self.entity_type} with id {entity_id}")
        return response.status_code == 204

    def links(self, entity_id: int) -> EntityLinksSchema:
        """Получить связи сущности.
        
        Доступно только для leads, contacts, companies, customers!
        """
        if self.get_entity_type() not in [
            "leads",
            "contacts", 
            "companies",
            "customers",
        ]:
            raise UnsupportedOperationError("links", self.get_entity_type())
            
        url = f"{self.get_base_url()}/{entity_id}/links"
        response = self.session.get(url)
        if response.status_code >= 400:
            self._handle_response_error(response, f"Get links for {self.entity_type} with id {entity_id}")
        
        return EntityLinksSchema(**response.json())

    def get_by_ids(self, entity_ids: List[int], **kwargs) -> List[T]:
        """Получить несколько сущностей по списку ID"""
        if not entity_ids:
            return []
        
        # AmoCRM поддерживает фильтр по нескольким ID через запятую
        params = kwargs.copy()
        params["filter[id]"] = ",".join(map(str, entity_ids))
        
        return self.get_all(**params)
