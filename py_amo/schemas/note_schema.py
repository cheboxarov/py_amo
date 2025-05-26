from typing import Optional, Dict, Any
from pydantic import BaseModel


class NoteSchema(BaseModel):
    id: Optional[int] = None
    entity_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    note_type: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    account_id: Optional[int] = None


class NoteInputSchema(BaseModel):
    entity_id: int
    note_type: str
    params: Optional[Dict[str, Any]] = None 