from src.core.infrastructure.repositories import InMemoryRepository
from src.inventory.domain.entities import Item
from src.inventory.domain.repositories import IItemRepository
from src.inventory.domain.value_objects import SKU


class FakeItemRepository(InMemoryRepository[Item], IItemRepository):
    """Fake Item Repository that satisfies IItemRepository for testing."""

    async def get_by_sku(self, sku: SKU) -> Item | None:
        """Find an item by SKU in the fake database."""
        for item in self._data.values():
            if item.sku == sku:
                return item

        return None
