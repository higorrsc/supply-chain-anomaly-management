from dataclasses import dataclass
from uuid import UUID

from src.inventory.domain.entities import Item
from src.inventory.domain.exceptions import ItemNotFoundError
from src.inventory.domain.repositories import IItemRepository


@dataclass(frozen=True)
class UpdateItemRequestDTO:
    """Data Transfer Object for update item requests."""

    id: UUID
    description: str


class UpdateItemUseCase:
    """Use case to update an existing item."""

    def __init__(self, repository: IItemRepository) -> None:
        """Initialize the use case."""

        self._repository = repository

    async def execute(self, request: UpdateItemRequestDTO) -> Item:
        """Execute the use case."""

        item = await self._repository.get_by_id(request.id)
        if item is None:
            raise ItemNotFoundError(f"Item with id {request.id} not found.")

        item.description = request.description
        item.validate()

        return await self._repository.update(item)
