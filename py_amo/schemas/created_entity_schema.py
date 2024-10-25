from pydantic import BaseModel, Field
from typing import Optional


class CreatedEntity(BaseModel):
    entity_type: str
    id: int
    link: Optional[str] = None