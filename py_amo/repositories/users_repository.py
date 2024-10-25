from schemas import UserSchema
from .base_repository import BaseRepository


class UsersRepository(BaseRepository[UserSchema]):
    
    REPOSITORY_PATH = "/api/v4/users"
    ENTITY_TYPE = "users"
    SCHEMA_CLASS = UserSchema