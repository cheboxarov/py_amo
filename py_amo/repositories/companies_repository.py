from py_amo.schemas import CompanySchema
from .base_repository import BaseRepository


class CompaniesRepository(BaseRepository[CompanySchema]):

    REPOSITORY_PATH = "/api/v4/companies"
    ENTITY_TYPE = "companies"
    SCHEMA_CLASS = CompanySchema
    SCHEMA_INPUT_CLASS = CompanySchema
