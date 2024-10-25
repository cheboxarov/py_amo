from schemas import ContactSchema
from repositories import BaseRepository


class ContactsRepository(BaseRepository[ContactSchema]):

    REPOSITORY_PATH = "/api/v4/contacts"
    ENTITY_TYPE = "contacts"
    SCHEMA_CLASS = ContactSchema