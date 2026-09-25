from .item_controller import router as item_router
from .movement_controller import router as movement_router
from .warehouse_controller import router as warehouse_router

__all__ = [
    "item_router",
    "movement_router",
    "warehouse_router",
]
