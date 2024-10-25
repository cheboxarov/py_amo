from py_amo.schemas import PipelineStatusSchema, PipelineStatusInputSchema
from .base_async_repository import BaseAsyncRepository


class PipelineStatusesAsyncRepository(BaseAsyncRepository[PipelineStatusSchema]):

    REPOSITORY_PATH = "/api/v4/leads/pipelines/{}/statuses"
    ENTITY_TYPE = "statuses"
    SCHEMA_CLASS = PipelineStatusSchema
    SCHEMA_INPUT_CLASS = PipelineStatusInputSchema

    def __init__(self, pipeline_id: int, *args, **kwargs):
        self.pipeline_id = pipeline_id
        super().__init__(*args, **kwargs)
    
    def get_base_url(self):
        return super().get_base_url().format(self.pipeline_id)
