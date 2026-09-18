from dataclasses import dataclass

from src.inventory.domain.entities import Item
from src.inventory.domain.repositories import IItemRepository
from src.inventory.domain.value_objects import SKU


@dataclass(frozen=True)
class GetItemBySKURequestDTO:
    """Data Transfer Object representing a SKU"""

    sku: SKU


class GetItemBySKUUseCase:
    """Use case to get an item by its SKU"""

    def __init__(
        self,
        repository: IItemRepository,
        not_found_exception: type[Exception],
        not_found_message: str = "Item with SKU {sku} not found.",
    ) -> None:
        """Initialize the use case"""

        self._repository = repository
        self._not_found_exception = not_found_exception
        self._not_found_message = not_found_message

    async def execute(self, request: GetItemBySKURequestDTO) -> Item:
        """Execute the use case"""

        entity = await self._repository.get_by_sku(sku=request.sku)
        if entity is None:
            raise self._not_found_exception(
                self._not_found_message.format(sku=request.sku)
            )

        return entity
