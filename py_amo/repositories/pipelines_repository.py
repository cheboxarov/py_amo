from schemas import PipelineSchema
from .base_repository import BaseRepository


class PipelinesRepository(BaseRepository[PipelineSchema]):

    REPOSITORY_PATH = "/api/v4/leads/pipelines"
    ENTITY_TYPE = "pipelines"
    SCHEMA_CLASS = PipelineSchema