from src.core.domain import AbstractRepository
from src.inventory.domain.entities import Warehouse


class IWarehouseRepository(AbstractRepository[Warehouse]):
    """Interface for the Warehouse Repository."""
