from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindQueryParameters
from app.core.dependencies import InventoryServiceDependency
from app.core.security import authorize
from app.models.models_enums import UserRoles
from app.schemas.inventory_schema import BaseInventory
from app.schemas.inventory_schema import FindInventoryResults
from app.schemas.inventory_schema import PublicInventory
from app.schemas.inventory_schema import UpdateInventory

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/", response_model=FindInventoryResults)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR, UserRoles.SELLER])
async def get_inventory_list(
    find_query: FindQueryParameters, service: InventoryServiceDependency, current_user: CurrentUserDependency
):
    return await service.get_list(find_query)


@router.get("/{inventory_id}", response_model=PublicInventory)
async def get_inventory_by_id(inventory_id: UUID, service: InventoryServiceDependency):
    return await service.get_by_id(inventory_id)


@router.post("/", status_code=201, response_model=PublicInventory)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR, UserRoles.BASE_USER])
async def create_inventory(
    inventory: BaseInventory, service: InventoryServiceDependency, current_user: CurrentUserDependency
):
    return await service.add(inventory)


@router.put("/{inventory_id}", response_model=PublicInventory)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR])
async def update_inventory(
    inventory_id: UUID,
    inventory: UpdateInventory,
    service: InventoryServiceDependency,
    current_user: CurrentUserDependency,
):
    return await service.patch(id=inventory_id, schema=inventory)


@router.delete("/{inventory_id}", status_code=204)
@authorize(role=[UserRoles.ADMIN, UserRoles.MODERATOR])
async def delete_inventory(
    inventory_id: UUID, service: InventoryServiceDependency, current_user: CurrentUserDependency
):
    return await service.remove_by_id(id=inventory_id)
