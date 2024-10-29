from pydantic import BaseModel, Field
from typing import Optional
from .custom_field_schema import CustomFieldShema


class ContactSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    is_deleted: Optional[bool] = None
    closest_task_at: Optional[int] = None
    custom_fields_values: Optional[list[CustomFieldShema]] = None
    account_id: Optional[int] = None
    emb: Optional[dict] = Field(alias="_embedded")
