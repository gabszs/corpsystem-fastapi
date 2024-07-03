from fastapi import APIRouter

from app.routes.v1.auth_routes import router as auth_router
from app.routes.v1.inventory_route import router as inventory_route
from app.routes.v1.ping_route import router as ping_router
from app.routes.v1.product_routes import router as product_router
from app.routes.v1.users_routes import router as user_router

routers = APIRouter(prefix="/v1")
router_list = [auth_router, inventory_route, product_router, user_router, ping_router]

for router in router_list:
    # router.tags = routers.tags.append("v1")
    routers.include_router(router)

__all__ = ["routers"]
