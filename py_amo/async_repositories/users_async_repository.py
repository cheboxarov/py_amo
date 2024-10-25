from py_amo.schemas import UserSchema
from .base_async_repository import BaseAsyncRepository


class UsersAsyncRepository(BaseAsyncRepository[UserSchema]):

    REPOSITORY_PATH = "/api/v4/users"
    ENTITY_TYPE = "users"
    SCHEMA_CLASS = UserSchema
    SCHEMA_INPUT_CLASS = UserSchema