from py_amo.schemas import SourceSchema
from .base_repository import BaseRepository


class SourcesRepository(BaseRepository[SourceSchema]):
    
    REPOSITORY_PATH = "/api/v4/sources"
    ENTITY_TYPE = "sources"
    SCHEMA_CLASS = SourceSchema