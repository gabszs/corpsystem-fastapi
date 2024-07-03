from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict

from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo


class BaseInventory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
    quantity: int
    unit_price: float


class BaseInventoryWithId(BaseInventory):
    id: UUID


class PublicInventory(ModelBaseInfo, BaseInventory):
    ...


class UpdateInventory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: Optional[UUID]
    quantity: Optional[int]
    unit_price: Optional[float]


class FindInventoryResults(FindModelResult):
    founds: List[PublicInventory]


# page: Annotated[int, Field(gt=0)] = settings.PAGE
