from pydantic import BaseModel
from typing import Optional, Dict


class CatalogElementSchema(BaseModel):
    id: Optional[int] = None
    metadata: Optional[Dict] = None
    quantity: Optional[float] = None
    catalog_id: Optional[int] = None
    price_id: Optional[int] = None