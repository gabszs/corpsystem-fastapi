


CODIGO UML
```
@startuml

!define Mapped(x) entity x
!define mapped_column(x) field x
!define back_populates(x) {back_populates x}

package "Models" {

  class User {
    password: Mapped[str]
    email: Mapped[str]
    username: Mapped[str]
    role: Mapped[UserRoles]
    is_active: Mapped[bool]

    sales: Mapped[List["Sale"]] # 1-n
    purchases: Mapped[List["Purchase"]] # 1-n
  }

  class Product {
    name: Mapped[str]
    description: Mapped[str]

    inventory: Mapped[List["Inventory"]] # 1-n
    sales_items: Mapped[List["SaleItem"]] # 1-n
    purchases: Mapped[List["Purchase"]] # 1-n
  }

  class Sale {
    seller_id: Mapped[UUID]

    seller: Mapped[User] # n-1
    items: Mapped[List["SaleItem"]] # 1-n
  }

  class SaleItem {
    sale_id: Mapped[UUID]
    product_id: Mapped[UUID]
    quantity: Mapped[int]
    unit_price: Mapped[float]
    total_price: Mapped[float]

    sale: Mapped[Sale] # n-1
    product: Mapped[Product] # n-1
  }

  class Purchase {
    buyer_id: Mapped[UUID]
    product_id: Mapped[UUID]
    quantity: Mapped[int]
    unit_price: Mapped[float]
    total_price: Mapped[float]

    buyer: Mapped[User] # n-1
    product: Mapped[Product] # n-1
  }

  class Inventory {
    product_id: Mapped[UUID]
    quantity: Mapped[int]
    unit_price: Mapped[float]

    product: Mapped[Product] # n-1
  }

  User "1" <--> "n" Sale : sales
  User "1" <--> "n" Purchase : purchases
  Product "1" <--> "n" Inventory : inventory
  Product "1" <--> "n" SaleItem : sales_items
  Product "1" <--> "n" Purchase : purchases
  Sale "1" <--> "n" SaleItem : items
}

@enduml
```
