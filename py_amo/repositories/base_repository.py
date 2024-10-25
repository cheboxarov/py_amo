from typing import TypeVar, Generic, Optional
from py_amo.schemas.entity_link_schema import EntityLinksSchema
from py_amo.schemas.created_entity_schema import CreatedEntity
from py_amo.services.filters import with_kwargs_filter
import json

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
        self.schema_input_class = self.SCHEMA_INPUT_CLASS

    def get_base_url(self) -> str:
        return self.base_url

    def get_entity_type(self) -> str:
        return self.entity_type

    @with_kwargs_filter
    def get_all(self, **kwargs) -> list[T]:

        """
        kwargs:

        - limit: int
        - with_: str (Смотреть в документации)
        - offset: int

        Чтобы узнать остальные параметры - обращайтесь к офф. документации.

        """
        response = self.session.get(self.get_base_url(), params=kwargs)
        response.raise_for_status()
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
        response.raise_for_status()
        return self.schema_class(**response.json())

    def create(self, entities: list[T]) -> list[CreatedEntity]:
        response = self.session.post(self.get_base_url(), data=json.dumps([entity.dict(exclude_none=True) for entity in entities]))
        response.raise_for_status()
        created_ids = [CreatedEntity(id=created_lead.get("id", None),
                                     entity_type=self.entity_type,
                                     link=created_lead.get("_links", {}).get("self", {}).get("href"))
                       for created_lead in 
                       response.json().get("_embedded", {}).get("leads", [])]
        return created_ids

    def update(self, entity: T) -> T:
        entity_data = entity.dict(exclude_none=True)
        entity_id = entity_data.pop("id")
        if entity_id is None:
            raise ValueError("entity need id")
        update_data = self.schema_input_class(**entity_data).dict(exclude_none=True)
        print(update_data)
        response = self.session.patch(self.get_base_url()+f"/{entity_id}", 
                                      json=update_data)
        print(response.json())
        response.raise_for_status()
        return self.schema_class(**response.json())

    def delete(self, entity_id: int):
        url = f"{self.get_base_url()}/{entity_id}"
        response = self.session.delete(url)
        response.raise_for_status()

    def links(self, entity_id: int):

        """

        Доступно только для leads, contacts, companies, customers!

        """

        if not self.get_entity_type() in ["leads", "contacts", "companies", "customers"]:
            raise ValueError(f"cant get links from this entity!")
        url = f"{self.get_base_url()}/{entity_id}/links"
        response = self.session.get(url)
        return EntityLinksSchema(**response.json())
