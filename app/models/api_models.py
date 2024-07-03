from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import Base
from app.models.models_enums import UserRoles


class User(Base):
    __tablename__ = "users"

    password: Mapped[str] = mapped_column(String(length=255))
    email: Mapped[str] = mapped_column(String(length=50), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)

    sales: Mapped[List["Sale"]] = relationship(back_populates="seller", cascade="all, delete-orphan", init=False)
    purchases: Mapped[List["Purchase"]] = relationship(back_populates="buyer", cascade="all, delete-orphan", init=False)
    role: Mapped[UserRoles] = mapped_column(default=UserRoles.BASE_USER, server_default=UserRoles.BASE_USER)
    is_active: Mapped[bool] = mapped_column(default=True)


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(length=100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(length=240))

    inventory: Mapped[List["Inventory"]] = relationship(back_populates="product", init=False)
    sales_items: Mapped[List["SaleItem"]] = relationship(back_populates="product", init=False)
    purchases: Mapped[List["Purchase"]] = relationship(back_populates="product", init=False)


class Sale(Base):
    __tablename__ = "sales"

    seller_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    seller: Mapped[User] = relationship(back_populates="sales")
    items: Mapped[List["SaleItem"]] = relationship(back_populates="sale")


class SaleItem(Base):
    __tablename__ = "sale_items"

    sale_id: Mapped[UUID] = mapped_column(ForeignKey("sales.id"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    unit_price: Mapped[float]
    total_price: Mapped[float]

    sale: Mapped[Sale] = relationship(back_populates="items")
    product: Mapped[Product] = relationship(back_populates="sales_items")


class Purchase(Base):
    __tablename__ = "purchases"

    buyer_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    unit_price: Mapped[float]
    total_price: Mapped[float]

    buyer: Mapped[User] = relationship(back_populates="purchases")
    product: Mapped[Product] = relationship(back_populates="purchases")


class Inventory(Base):
    __tablename__ = "inventory"

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), unique=True, index=True)
    quantity: Mapped[int]
    unit_price: Mapped[float]
    product: Mapped[Product] = relationship(back_populates="inventory", init=False)
