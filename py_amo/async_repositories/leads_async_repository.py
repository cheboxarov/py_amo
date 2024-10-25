from py_amo.schemas import LeadSchema
from .base_async_repository import BaseAsyncRepository


class LeadsAsyncRepository(BaseAsyncRepository[LeadSchema]):

    REPOSITORY_PATH = "/api/v4/leads"
    ENTITY_TYPE = "leads"
    SCHEMA_CLASS = LeadSchema
    SCHEMA_INPUT_CLASS = LeadSchema