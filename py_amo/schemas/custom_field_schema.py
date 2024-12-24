from pydantic import BaseModel
from typing import Optional


class CustomFieldValues(BaseModel):
    value: Optional[str | int] = None
    enum_id: Optional[int] = None
    enum_code: Optional[str] = None


class CustomFieldShema(BaseModel):
    field_id: Optional[int] = None
    field_name: Optional[str] = None
    field_code: Optional[str] = None
    field_type: Optional[str] = None
    values: Optional[list[CustomFieldValues]] = None
    account_id: Optional[int] = None
