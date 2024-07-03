from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindQueryParameters
from app.core.dependencies import ProductServiceDependency
from app.core.security import authorize
from app.models.models_enums import UserRoles
from app.schemas.product_schema import BaseProduct
from app.schemas.product_schema import FindProductResults
from app.schemas.product_schema import PublicProduct
from app.schemas.product_schema import UpdateProduct

router = APIRouter(prefix="/product", tags=["product"])


@router.get("/", response_model=FindProductResults)
async def get_product_list(
    find_query: FindQueryParameters, service: ProductServiceDependency, current_user: CurrentUserDependency
):
    return await service.get_list(find_query)


@router.get("/{product_id}", response_model=PublicProduct)
async def get_product_by_id(product_id: UUID, service: ProductServiceDependency):
    return await service.get_by_id(product_id)


@router.post("/", status_code=201, response_model=PublicProduct)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR, UserRoles.SELLER])
async def create_product(product: BaseProduct, service: ProductServiceDependency, current_user: CurrentUserDependency):
    return await service.add(product)


@router.put("/{product_id}", response_model=PublicProduct)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR])
async def update_product(
    product_id: UUID, product: UpdateProduct, service: ProductServiceDependency, current_user: CurrentUserDependency
):
    return await service.patch(id=product_id, schema=product)


@router.delete("/{product_id}", status_code=204)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR])
async def delete_product(product_id: UUID, service: ProductServiceDependency, current_user: CurrentUserDependency):
    return await service.remove_by_id(id=product_id)
