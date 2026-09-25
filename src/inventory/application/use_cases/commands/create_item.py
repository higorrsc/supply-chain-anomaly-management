from dataclasses import dataclass

from src.core.domain import ConflictError
from src.inventory.domain.entities import Item
from src.inventory.domain.repositories import IItemRepository
from src.inventory.domain.value_objects import SKU


@dataclass(frozen=True)
class CreateItemRequestDTO:
    """Data Transfer Object for create item requests."""

    sku: str
    description: str
    is_active: bool = True


class CreateItemUseCase:
    """Use case to create a new item."""

    def __init__(self, repository: IItemRepository) -> None:
        """Initialize the use case."""

        self._repository = repository

    async def execute(self, request: CreateItemRequestDTO) -> Item:
        """Execute the use case."""

        sku = SKU(value=request.sku)

        existing_item = await self._repository.get_by_sku(sku)
        if existing_item is not None:
            raise ConflictError(f"Item with SKU {request.sku} already exists.")

        item = Item(
            sku=sku,
            description=request.description,
            is_active=request.is_active,
        )
        return await self._repository.save(item)
