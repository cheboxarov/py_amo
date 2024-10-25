from typing import TypeVar, Generic, Optional, List
from py_amo.schemas.entity_link_schema import EntityLinksSchema
from py_amo.schemas.created_entity_schema import CreatedEntity
from py_amo.services.filters import with_kwargs_filter
import json
import httpx
from py_amo.utils.async_utils import repository_safe_request
import asyncio

T = TypeVar('T')

class BaseAsyncRepository(Generic[T]):
    def __init__(self, session):
        """
        session - AmoSession
        """
        self.session = session.get_async_session()
        self.base_url = session.get_url() + self.REPOSITORY_PATH
        self.entity_type = self.ENTITY_TYPE
        self.schema_class = self.SCHEMA_CLASS
        self.schema_input_class = self.SCHEMA_INPUT_CLASS
        self.subdomain = session.get_subdomain()
        self.amo_session = session

    def get_base_url(self) -> str:
        return self.base_url

    def get_entity_type(self) -> str:
        return self.entity_type

    @with_kwargs_filter
    async def get_all(self, **kwargs) -> List[T]:
        """
        kwargs:
        - limit: int
        - with_: str (Смотреть в документации)
        - offset: int
        """

        if (limit := kwargs.get("limit", 0)) > 250:
            def divide_number(number, max_value):
                parts = []
                while number > 0:
                    part = min(max_value, number)
                    parts.append(part)
                    number -= part
                return parts
            
            kwargs.pop("limit")
            semaphore = asyncio.Semaphore(7)
            result = await asyncio.gather(*(repository_safe_request(self.get_all, semaphore, i, **kwargs, page=i, limit=chunk_limit) for i, chunk_limit in enumerate(divide_number(limit,250))))
            entities = []
            for chunk_entities in result:
                entities += chunk_entities
            return entities
        
        response = await self.session.get(self.get_base_url(), params=kwargs)
        response.raise_for_status()
        data = response.json()
        row_entities = data.get("_embedded", {}).get(self.get_entity_type(), [])
        return [self.schema_class(**item) for item in row_entities]

    @with_kwargs_filter
    async def get_by_id(self, entity_id: int, **kwargs) -> Optional[T]:
        """
        kwargs:
        - with_: str (Смотреть в документации)
        """
        url = f"{self.get_base_url()}/{entity_id}"
        response = await self.session.get(url, params=kwargs)
        if response.status_code in [404, 204]:
            return None
        response.raise_for_status()
        return self.schema_class(**response.json())

    async def create(self, entities: List[T]) -> List[CreatedEntity]:
        payload = json.dumps([entity.dict(exclude_none=True) for entity in entities])
        response = await self.session.post(self.get_base_url(), data=payload)
        response.raise_for_status()
        created_ids = [
            CreatedEntity(
                id=created_entity.get("id"),
                entity_type=self.entity_type,
                link=created_entity.get("_links", {}).get("self", {}).get("href")
            )
            for created_entity in response.json().get("_embedded", {}).get("leads", [])
        ]
        return created_ids

    async def update(self, entity: T) -> T:
        entity_data = entity.dict(exclude_none=True)
        entity_id = entity_data.pop("id", None)
        if entity_id is None:
            raise ValueError("entity needs an id")
        
        update_data = self.schema_input_class(**entity_data).dict(exclude_none=True)
        url = f"{self.get_base_url()}/{entity_id}"
        response = await self.session.patch(url, json=update_data)
        response.raise_for_status()
        return self.schema_class(**response.json())

    async def delete(self, entity_id: int):
        url = f"{self.get_base_url()}/{entity_id}"
        response = await self.session.delete(url)
        response.raise_for_status()

    async def links(self, entity_id: int) -> EntityLinksSchema:
        """
        Доступно только для leads, contacts, companies, customers!
        """
        if self.get_entity_type() not in ["leads", "contacts", "companies", "customers"]:
            raise ValueError("Can't get links from this entity!")

        url = f"{self.get_base_url()}/{entity_id}/links"
        response = await self.session.get(url)
        response.raise_for_status()
        return EntityLinksSchema(**response.json())
