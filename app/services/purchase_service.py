from typing import Union
from uuid import UUID

from app.repository import PurchaseRepository
from app.schemas.purchase_schema import BasePurchase
from app.schemas.purchase_schema import PurchaseWithTotalPrice
from app.services.base_service import BaseService


class PurchaseService(BaseService):
    def __init__(self, purchase_repository: PurchaseRepository):
        self.purchase_repository = purchase_repository
        super().__init__(purchase_repository)

    async def add(self, schema: BasePurchase, **kwargs):
        purchase = PurchaseWithTotalPrice(total_price=schema.quantity * schema.unit_price, **schema.model_dump())
        return await self._repository.create(purchase, **kwargs)

    async def patch(self, id: Union[UUID, int], schema, **kwargs):
        purchase = PurchaseWithTotalPrice(total_price=schema.quantity * schema.unit_price, **schema.model_dump())
        return await self._repository.update(id, purchase, **kwargs)
