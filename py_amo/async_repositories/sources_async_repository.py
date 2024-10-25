from py_amo.schemas import SourceSchema
from .base_async_repository import BaseAsyncRepository


class SourcesAsyncRepository(BaseAsyncRepository[SourceSchema]):
    
    REPOSITORY_PATH = "/api/v4/sources"
    ENTITY_TYPE = "sources"
    SCHEMA_CLASS = SourceSchema
    SCHEMA_INPUT_CLASS = SourceSchema