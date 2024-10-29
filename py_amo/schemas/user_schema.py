from typing import Optional, List
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    lang: Optional[str] = None
    rights: Optional[dict] = None
    amojo_id: Optional[str] = None
    uuid: Optional[str] = None
    role: Optional[str] = None
