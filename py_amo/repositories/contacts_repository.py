from py_amo.schemas import ContactSchema
from py_amo.repositories import BaseRepository


class ContactsRepository(BaseRepository[ContactSchema]):

    REPOSITORY_PATH = "/api/v4/contacts"
    ENTITY_TYPE = "contacts"
    SCHEMA_CLASS = ContactSchema
    SCHEMA_INPUT_CLASS = ContactSchema
