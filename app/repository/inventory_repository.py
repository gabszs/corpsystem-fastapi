from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError
from app.core.exceptions import DuplicatedError
from app.core.exceptions import ValidationError
from app.models import Inventory
from app.repository.base_repository import BaseRepository


class InventoryRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Inventory)

    async def create(self, schema):
        async with self.session_factory() as session:
            model = self.model(**schema.model_dump())
            try:
                session.add(model)
                await session.commit()
                await session.refresh(model)

            except IntegrityError as _:
                model_name = "Inventory"
                if "Cannot add or update a child row" in str(_):
                    raise ValidationError("Wrong FK ID, please use correct model FK")
                raise DuplicatedError(detail=f"{model_name} already registered")
            except Exception as error:
                raise BadRequestError(str(error))
            return model
