from src.core.domain import AbstractRepository
from src.inventory.domain.entities import Item
from src.inventory.domain.value_objects import SKU


class IItemRepository(AbstractRepository[Item]):
    """Interface for the Item Repository."""

    async def get_by_sku(self, sku: SKU) -> Item | None:
        """Get an Item by SKU"""

        raise NotImplementedError
