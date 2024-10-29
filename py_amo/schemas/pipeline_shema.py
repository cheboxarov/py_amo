from pydantic import BaseModel, Field
from typing import Optional, List
from .pipeline_status_schema import PipelineStatusSchema


class PipelineSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    sort: Optional[int] = None
    is_main: Optional[bool] = None
    is_unsorted_on: Optional[bool] = None
    is_archive: Optional[bool] = None
    account_id: Optional[int] = None
    emb: Optional[dict] = Field(alias="_embedded")

    @property
    def statuses(self) -> Optional[List[PipelineStatusSchema]]:
        if self.emb and "statuses" in self.emb:
            return [PipelineStatusSchema(**status) for status in self.emb["statuses"]]
        return None
