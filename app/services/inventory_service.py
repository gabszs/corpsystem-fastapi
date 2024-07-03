from app.repository import InventoryRepository
from app.services.base_service import BaseService


class InventoryService(BaseService):
    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository
        super().__init__(inventory_repository)
