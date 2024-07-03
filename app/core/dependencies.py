from typing import Annotated
from uuid import UUID

from fastapi import Depends
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.database import get_session_factory
from app.core.exceptions import AuthError
from app.core.security import JWTBearer
from app.core.settings import settings
from app.models import User
from app.repository import InventoryRepository
from app.repository import ProductRepository
from app.repository import UserRepository
from app.schemas.auth_schema import Payload
from app.schemas.base_schema import FindBase
from app.services import AuthService
from app.services import InventoryService
from app.services import ProductService
from app.services import UserService


async def get_user_service(session: AsyncSession = Depends(get_session_factory)):
    user_repository = UserRepository(session_factory=session)
    return UserService(user_repository)


async def get_current_user(token: str = Depends(JWTBearer()), service: UserService = Depends(get_user_service)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    current_user: User = await service.get_by_id(UUID(token_data.id))  # type: ignore
    if not current_user:
        raise AuthError(detail="User not found")
    return current_user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


async def get_auth_service(session: AsyncSession = Depends(get_session_factory)):
    user_repository = UserRepository(session_factory=session)
    return AuthService(user_repository=user_repository)


async def get_product_service(session: AsyncSession = Depends(get_session_factory)):
    product_repository = ProductRepository(session_factory=session)
    return ProductService(product_repository)


async def get_inventory_service(session: AsyncSession = Depends(get_session_factory)):
    inventory_repository = InventoryRepository(session_factory=session)
    return InventoryService(inventory_repository)


FindQueryParameters = Annotated[FindBase, Depends()]
SessionDependency = Annotated[Session, Depends(get_db)]
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
CurrentActiveUserDependency = Annotated[User, Depends(get_current_active_user)]
ProductServiceDependency = Annotated[ProductService, Depends(get_product_service)]
InventoryServiceDependency = Annotated[InventoryService, Depends(get_inventory_service)]
