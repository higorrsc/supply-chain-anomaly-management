from dataclasses import dataclass

from src.inventory.domain.entities import Warehouse
from src.inventory.domain.repositories import IWarehouseRepository


@dataclass(frozen=True)
class CreateWarehouseRequestDTO:
    """Data Transfer Object for create warehouse requests."""

    name: str
    location_code: str
    is_active: bool = True


class CreateWarehouseUseCase:
    """Use case to create a new warehouse."""

    def __init__(self, repository: IWarehouseRepository) -> None:
        """Initialize the use case."""

        self._repository = repository

    async def execute(self, request: CreateWarehouseRequestDTO) -> Warehouse:
        """Execute the use case."""

        warehouse = Warehouse(
            name=request.name,
            location_code=request.location_code,
            is_active=request.is_active,
        )
        return await self._repository.save(warehouse)
