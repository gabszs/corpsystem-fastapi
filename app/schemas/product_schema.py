from typing import Annotated
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo


class BaseProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Annotated[str, Field(max_length=50)]
    description: Annotated[str, Field(max_length=50)]


class BaseProductWithId(BaseProduct):
    id: UUID


class PublicProduct(ModelBaseInfo, BaseProduct):
    ...


class UpdateProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Annotated[Optional[str], Field(max_length=50)]
    description: Annotated[Optional[str], Field(max_length=50)]


class FindProductResults(FindModelResult):
    founds: List[PublicProduct]


# page: Annotated[int, Field(gt=0)] = settings.PAGE
