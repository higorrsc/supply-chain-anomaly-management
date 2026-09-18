from src.core.infrastructure.repository import InMemoryRepository
from src.inventory.domain.entities import Warehouse
from src.inventory.domain.repositories import IWarehouseRepository


class FakeWarehouseRepository(InMemoryRepository[Warehouse], IWarehouseRepository):
    """Fake Warehouse Repository that satisfies IWarehouseRepository for testing."""
