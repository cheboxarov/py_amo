from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class TaskTypeSchema(BaseModel):
    id: int
    name: str
    color: Optional[str] = None
    icon_id: Optional[int] = None
    code: Optional[str] = None


class TaskSchema(BaseModel):
    id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
    is_completed: Optional[bool] = None
    task_type_id: Optional[int] = None
    text: Optional[str] = None
    duration: Optional[int] = None
    complete_till: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    account_id: Optional[int] = None


class TaskInputSchema(BaseModel):
    responsible_user_id: Optional[int] = None
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
    is_completed: Optional[bool] = None
    task_type_id: Optional[int] = None
    text: Optional[str] = None
    duration: Optional[int] = None
    complete_till: Optional[int] = None
    result: Optional[Dict[str, Any]] = None 