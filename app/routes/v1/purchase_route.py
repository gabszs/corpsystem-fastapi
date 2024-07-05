from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindQueryParameters
from app.core.dependencies import PurchaseServiceDependency
from app.core.security import authorize
from app.models.models_enums import UserRoles
from app.schemas.purchase_schema import FindPurchaseResults
from app.schemas.purchase_schema import PublicPurchase
from app.schemas.purchase_schema import UpdatePurchase

router = APIRouter(prefix="/purchase", tags=["purchase"])


@router.get("/", response_model=FindPurchaseResults)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR, UserRoles.BUYER])
async def get_purchase_list(
    find_query: FindQueryParameters, service: PurchaseServiceDependency, current_user: CurrentUserDependency
):
    return await service.get_list(find_query)


@router.get("/{purchase_id}", response_model=PublicPurchase)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR, UserRoles.BUYER])
async def get_purchase_by_id(
    purchase_id: UUID, service: PurchaseServiceDependency, current_user: CurrentUserDependency
):
    return await service.get_by_id(purchase_id)


@router.post("/", status_code=201, response_model=PublicPurchase)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR, UserRoles.BUYER])
async def create_purchase(
    purchase: UpdatePurchase, service: PurchaseServiceDependency, current_user: CurrentUserDependency
):
    return await service.add(purchase)


@router.put("/{purchase_id}", response_model=PublicPurchase)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR])
async def update_purchase(
    purchase_id: UUID,
    purchase: UpdatePurchase,
    service: PurchaseServiceDependency,
    current_user: CurrentUserDependency,
):
    return await service.patch(id=purchase_id, schema=purchase)


@router.delete("/{purchase_id}", status_code=204)
@authorize(role=[UserRoles.ADMIN])
async def delete_purchase(purchase_id: UUID, service: PurchaseServiceDependency, current_user: CurrentUserDependency):
    return await service.remove_by_id(id=purchase_id)
