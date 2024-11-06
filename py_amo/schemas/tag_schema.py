from pydantic import BaseModel
from typing import Optional


class TagSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    color: Optional[str] = None
