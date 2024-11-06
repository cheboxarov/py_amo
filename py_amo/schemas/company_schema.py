from pydantic import BaseModel, Field
from typing import Optional, List
from .tag_schema import TagSchema
from .custom_field_schema import CustomFieldShema
from .catalog_element_schema import CatalogElementSchema

class ContactInfoSchema(BaseModel):
    id: Optional[int] = None

class CustomerInfoSchema(BaseModel):
    id: Optional[int] = None

class LeadInfoSchema(BaseModel):
    id: Optional[int] = None

class EmbeddedSchema(BaseModel):
    tags: Optional[List[TagSchema]] = None
    contacts: Optional[List[ContactInfoSchema]] = None
    customers: Optional[List[CustomerInfoSchema]] = None
    leads: Optional[List[LeadInfoSchema]] = None
    catalog_elements: Optional[List[CatalogElementSchema]] = None

class CompanySchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    closest_task_at: Optional[int] = None
    custom_fields_values: Optional[List[CustomFieldShema]] = None
    is_deleted: Optional[bool] = None
    account_id: Optional[int] = None
    emb: Optional[EmbeddedSchema] = Field(alias="_embedded")