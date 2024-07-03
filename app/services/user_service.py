from app.core.security import get_password_hash
from app.repository import UserRepository
from app.schemas.user_schema import BaseUserWithPassword
from app.services.base_service import BaseService
from app.services.base_service import FindBase


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def get_list(self, schema: FindBase):  # type: ignore
        return await self._repository.read_by_options(schema, unique=True)

    async def add(self, user_schema: BaseUserWithPassword):  # type: ignore
        user_schema.password = get_password_hash(user_schema.password)
        created_user = await self._repository.create(user_schema)
        delattr(created_user, "password")
        return created_user
