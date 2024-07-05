from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Purchase
from app.repository.base_repository import BaseRepository


class PurchaseRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Purchase)
