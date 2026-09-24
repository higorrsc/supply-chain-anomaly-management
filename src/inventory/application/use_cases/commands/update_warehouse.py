from dataclasses import dataclass
from uuid import UUID

from src.inventory.domain.entities import Warehouse
from src.inventory.domain.exceptions import WarehouseNotFoundError
from src.inventory.domain.repositories import IWarehouseRepository


@dataclass(frozen=True)
class UpdateWarehouseRequestDTO:
    """Data Transfer Object for update warehouse requests."""

    id: UUID
    name: str
    location_code: str


class UpdateWarehouseUseCase:
    """Use case to update an existing warehouse."""

    def __init__(self, repository: IWarehouseRepository) -> None:
        """Initialize the use case."""

        self._repository = repository

    async def execute(self, request: UpdateWarehouseRequestDTO) -> Warehouse:
        """Execute the use case."""

        warehouse = await self._repository.get_by_id(request.id)
        if warehouse is None:
            raise WarehouseNotFoundError(f"Warehouse with id {request.id} not found.")

        warehouse.name = request.name
        warehouse.location_code = request.location_code
        warehouse.validate()

        return await self._repository.update(warehouse)
