from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict

from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo


class BasePurchase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    buyer_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float


class BasePurchaseWithId(BasePurchase):
    id: UUID


class UpdatePurchase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    buyer_id: Optional[UUID]
    product_id: Optional[UUID]
    quantity: Optional[int]
    unit_price: Optional[float]


class PurchaseWithTotalPrice(UpdatePurchase):
    total_price: float


class PublicPurchase(ModelBaseInfo, PurchaseWithTotalPrice):
    ...


class FindPurchaseResults(FindModelResult):
    founds: List[PublicPurchase]


# page: Annotated[int, Field(gt=0)] = settings.PAGE
