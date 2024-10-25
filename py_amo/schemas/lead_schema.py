from pydantic import BaseModel, Field
from typing import Optional
from .custom_field_schema import CustomFieldShema


class LeadSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[int] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    status_id: Optional[int] = None
    pipeline_id: Optional[int] = None
    loss_reason_id: Optional[int] = None
    source_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    closed_at: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    closest_task_at: Optional[int] = None 
    is_deleted: Optional[bool] = None
    custom_fields_values: Optional[list[CustomFieldShema]] = None
    score: Optional[int] = None
    account_id: Optional[int] = None
    embedded: Optional[dict] = Field(alias="_embedded")
