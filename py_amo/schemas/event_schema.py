from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class EventValueAfterSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class EventValueBeforeSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class EventSchema(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[int] = None
    value_after: Optional[List[EventValueAfterSchema]] = None
    value_before: Optional[List[EventValueBeforeSchema]] = None
    account_id: Optional[int] = None 