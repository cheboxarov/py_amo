from py_amo.schemas import PipelineSchema
from .base_async_repository import BaseAsyncRepository


class PipelinesAsyncRepository(BaseAsyncRepository[PipelineSchema]):

    REPOSITORY_PATH = "/api/v4/leads/pipelines"
    ENTITY_TYPE = "pipelines"
    SCHEMA_CLASS = PipelineSchema
    SCHEMA_INPUT_CLASS = PipelineSchema