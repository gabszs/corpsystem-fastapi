from app.repository import ProductRepository
from app.services.base_service import BaseService


class ProductService(BaseService):
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        super().__init__(product_repository)
