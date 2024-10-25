from pydantic import BaseModel, Field
from typing import Optional, Any


class MetadataSchema(BaseModel):
    main_contact: Optional[bool] = None
    quantity: Optional[float] = None
    catalog_id: Optional[int] = None
    price_id: Optional[Optional[int]] = None


class EntityLinksSchema(BaseModel):
    link_to_entity_id: int
    to_entity_type: str
    metadata: Optional[MetadataSchema] = None
