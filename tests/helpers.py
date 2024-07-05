from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.core.settings import settings
from app.models import User
from app.models.models_enums import UserRoles
from app.schemas.inventory_schema import PublicInventory
from app.schemas.product_schema import PublicProduct
from app.schemas.purchase_schema import PublicPurchase
from tests.factories import create_factory_users
from tests.factories import InventoryFactory
from tests.factories import ProductFactory
from tests.factories import PurchaseFactory
from tests.schemas import UserModelSetup
from tests.schemas import UserSchemaWithHashedPassword


def validate_datetime(data_string):
    try:
        datetime.strptime(data_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except ValueError:
        try:
            datetime.strptime(data_string, "%Y-%m-%dT%H:%M:%S")
            return True
        except ValueError:
            return False


async def add_users_models(
    session: AsyncSession,
    users_qty: int = 1,
    user_role: UserRoles = UserRoles.BASE_USER,
    is_active=True,
    index: Optional[int] = None,
    get_model: bool = False,
) -> Union[List[Union[UserSchemaWithHashedPassword, User]], UserSchemaWithHashedPassword, User]:
    return_users: List[Union[UserSchemaWithHashedPassword, User]] = []
    users = create_factory_users(users_qty=users_qty, user_role=user_role, is_active=is_active)
    password_list = [factory_model.password for factory_model in users]
    for user in users:
        user.password = get_password_hash(user.password)
    session.add_all(users)
    await session.commit()
    for count, user in enumerate(users):
        await session.refresh(user)
        if get_model:
            return_users.append(user)
            continue
        return_users.append(
            UserSchemaWithHashedPassword(
                id=user.id,
                created_at=user.created_at,
                updated_at=user.updated_at,
                email=user.email,
                username=user.username,
                is_active=user.is_active,
                role=user.role,
                password=password_list[count],
                hashed_password=user.password,
            )
        )

    if index is not None:
        return return_users[index]
    return return_users


async def setup_users_data(
    session: AsyncSession, model_args: List[UserModelSetup], **kwargs
) -> List[UserSchemaWithHashedPassword]:  # type: ignore
    return_list: List[UserSchemaWithHashedPassword] = []
    for user_setup in model_args:
        user_list = await add_users_models(
            session, users_qty=user_setup.qty, user_role=user_setup.role, is_active=user_setup.is_active, **kwargs
        )
        return_list.append(*user_list)
    return return_list


async def setup_product_data(
    session: AsyncSession, product_qty: int = 1, index: Optional[int] = None
) -> List[PublicProduct]:
    product_list: List[PublicProduct] = []
    products = ProductFactory.create_batch(product_qty)
    session.add_all(products)
    await session.commit()
    for product in products:
        await session.refresh(product)
        product_list.append(
            PublicProduct(
                name=product.name,
                description=product.description,
                id=product.id,
                created_at=product.created_at,
                updated_at=product.updated_at,
            )
        )

    if index is not None:
        return product_list[index]
    return product_list


async def setup_inventory_data(
    session: AsyncSession, inventory_qty: int = 1, index: Optional[int] = None
) -> List[PublicInventory]:
    inventory_list: List[PublicInventory] = []
    products = await setup_product_data(session, inventory_qty)
    inventory = []
    for product in products:
        inventory.append(InventoryFactory(product_id=product.id))

    session.add_all(inventory)
    await session.commit()
    for product in inventory:
        await session.refresh(product)
        inventory_list.append(
            PublicInventory(
                quantity=product.quantity,
                unit_price=product.unit_price,
                product_id=product.product_id,
                id=product.id,
                created_at=product.created_at,
                updated_at=product.updated_at,
            )
        )

    if index is not None:
        return inventory_list[index]
    return inventory_list


async def setup_purchase_data(
    session: AsyncSession, purchase_qty: int = 1, index: Optional[int] = None, multiple_assoc_models: bool = False
) -> Union[List[PublicPurchase], PublicPurchase]:
    purchases_list: List[PublicPurchase] = []
    purchases = []

    if multiple_assoc_models:
        products = await setup_product_data(session, purchase_qty)
        buyers = await add_users_models(session, users_qty=purchase_qty, user_role=UserRoles.BUYER)
        for buyer, product in zip(buyers, products):
            purchases.append(PurchaseFactory(product_id=product.id, buyer_id=buyer.id))
    else:
        product = (await setup_product_data(session, 1))[0]
        buyer = (await add_users_models(session, 1, user_role=UserRoles.BUYER))[0]
        purchases.extend(PurchaseFactory.create_batch(size=purchase_qty, product_id=product.id, buyer_id=buyer.id))

    session.add_all(purchases)
    await session.commit()
    for product in purchases:
        await session.refresh(product)
        purchases_list.append(
            PublicPurchase(
                quantity=product.quantity,
                unit_price=product.unit_price,
                product_id=product.product_id,
                buyer_id=product.buyer_id,
                total_price=product.total_price,
                id=product.id,
                created_at=product.created_at,
                updated_at=product.updated_at,
            )
        )

    if index is not None:
        return purchases_list[index]
    return purchases_list


async def token(client, session: AsyncSession, base_auth_route: str = "/v1/auth", **kwargs):
    user = await add_users_models(session=session, index=0, **kwargs)
    response = await client.post(
        f"{base_auth_route}/sign-in",
        json={"email__eq": user.email, "password": user.password},  # type: ignore
    )  # type: ignore
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


async def get_user_token(client: AsyncClient, user: UserSchemaWithHashedPassword) -> Dict[str, str]:
    response = await client.post(
        f"{settings.base_auth_route}/sign-in", json={"email__eq": user.email, "password": user.password}
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


async def get_user_by_index(client, index: int = 0, token_header: Optional[str] = None):
    response = await client.get(f"{settings.base_users_url}/?ordering=username", headers=token_header)
    return response.json()["founds"][index]


def validate_users_output_models(input_models: List[Any], output_models: List[Any], attrs_to_check: List[str]):
    for input_model in input_models:
        for output_model in output_models:
            if input_model.id == output_model["id"]:
                for attr in attrs_to_check:
                    if attr == "id":
                        assert str(input_model.getattr(attr)) == output_model["attr"]
                    assert input_model.getattr(attr) == output_model["attr"]


# def validate_users_output_models(input_models: List[str], output_models: List[str], attrs_to_check: List[str]):
#     for input_model in input_models:
#         for output_model in output_models:
#             if input_model.id == output_model["id"]:
#                 for attr in attrs_to_check:
#                     if attr == "id":
#                         assert str(input_model.getattr(attr)) == output_model["attr"]
#                     assert input_model.getattr(attr) == output_model["attr"]
