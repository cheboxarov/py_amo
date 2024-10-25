from typing import TypeVar, Generic, Optional
from py_amo.schemas.entity_link_schema import EntityLinksSchema
from py_amo.services.filters import with_kwargs_filter

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session):
        """
        session - AmoSession
        """
        self.session = session.get_requests_session()
        self.base_url = session.get_url()+self.REPOSITORY_PATH
        self.entity_type = self.ENTITY_TYPE
        self.schema_class = self.SCHEMA_CLASS

    @with_kwargs_filter
    def get_all(self, **kwargs) -> list[T]:

        if "with_" in kwargs.keys():
            kwargs["with"] = kwargs["with_"]
            del kwargs["with_"]
        response = self.session.get(self.base_url, params=kwargs)
        response.raise_for_status()
        data = response.json()
        row_entities = data.get("_embedded", {}).get(self.entity_type, [])
        return [self.schema_class(**item) for item in row_entities]

    @with_kwargs_filter
    def get_by_id(self, entity_id: int, **kwargs) -> Optional[T]:
        url = f"{self.base_url}/{entity_id}"
        response = self.session.get(url, params=kwargs)
        if response.status_code in [404, 204]:
            return None
        response.raise_for_status()
        return self.schema_class(**response.json())

    def create(self, entity_data: dict) -> T:
        response = self.session.post(self.base_url, json=entity_data)
        response.raise_for_status()
        return self.schema_class(**response.json())

    def delete(self, entity_id: int):
        url = f"{self.base_url}/{entity_id}"
        response = self.session.delete(url)
        response.raise_for_status()

    def links(self, entity_id: int):
        if not self.entity_type in ["leads", "contacts", "companies", "customers"]:
            raise ValueError(f"cant get links from this entity!")
        url = f"{self.base_url}/{entity_id}/links"
        response = self.session.get(url)
        return EntityLinksSchema(**response.json())
