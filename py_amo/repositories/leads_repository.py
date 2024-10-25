from schemas import LeadSchema
from .base_repository import BaseRepository


class LeadsRepository(BaseRepository[LeadSchema]):

    REPOSITORY_PATH = "/api/v4/leads"
    ENTITY_TYPE = "leads"
    SCHEMA_CLASS = LeadSchema