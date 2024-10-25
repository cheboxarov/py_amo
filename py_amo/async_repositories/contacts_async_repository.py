from py_amo.schemas import ContactSchema
from py_amo.async_repositories import BaseAsyncRepository


class ContactsAsyncRepository(BaseAsyncRepository[ContactSchema]):

    REPOSITORY_PATH = "/api/v4/contacts"
    ENTITY_TYPE = "contacts"
    SCHEMA_CLASS = ContactSchema
    SCHEMA_INPUT_CLASS = ContactSchema