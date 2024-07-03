from random import randint
from random import uniform
from typing import Any
from typing import Dict

import factory
from factory.base import StubObject

from app.models import Inventory
from app.models import Product
from app.models import User
from app.models.models_enums import UserRoles


def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
    stub_dict = stub.__dict__
    for key, value in stub_dict.items():
        if isinstance(value, StubObject):
            stub_dict[key] = convert_dict_from_stub(value)
    return stub_dict


def factory_object_to_dict(factory_instance):
    attributes = factory_instance.__dict__
    attributes.pop("_declarations", None)
    return attributes


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f"user_{x}")
    email = factory.LazyAttribute(lambda x: f"{x.username}@test.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.username}_password")
    role = UserRoles.BASE_USER
    is_active = None


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda x: f"product_{x}")
    description = factory.LazyAttribute(lambda x: f"{x.name}_description")


class InventoryFactory(factory.Factory):
    class Meta:
        model = Inventory

    product_id = None
    quantity = randint(1, 100000)
    unit_price = uniform(1, 100000)


def create_factory_users(users_qty: int = 1, user_role: UserRoles = UserRoles.BASE_USER, is_active=True):
    return UserFactory.create_batch(users_qty, role=user_role, is_active=is_active)
