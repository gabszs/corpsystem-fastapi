from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DuplicatedError
from app.models import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    async def create(self, schema):
        async with self.session_factory() as session:
            model = self.model(**schema.model_dump())
            try:
                session.add(model)
                await session.commit()
                await session.refresh(model)
            except IntegrityError as e:
                if "email" in str(e.orig):
                    raise DuplicatedError(detail="Email already registered")
                if "username" in str(e.orig):
                    raise DuplicatedError(detail="Username already registered")
                print(e.orig)
                print("caindo no ultimo try")
                raise DuplicatedError(detail=f"{self.model.__tablename__.capitalize()[:-1]} already registered")
            return model
