from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.core.domain.events import EventDispatcher
from src.inventory.domain.entities import Movement
from src.inventory.domain.enums import MovementType
from src.inventory.domain.exceptions import ItemNotFoundError, WarehouseNotFoundError
from src.inventory.domain.repositories import (
    IItemRepository,
    IMovementRepository,
    IWarehouseRepository,
)
from src.inventory.domain.value_objects import Quantity


@dataclass(frozen=True)
class CreateMovementRequestDTO:
    """Data Transfer Object for create movement requests."""

    item_id: UUID
    warehouse_id: UUID
    quantity: Decimal
    movement_type: str
    occurred_at: datetime


class CreateMovementUseCase:
    """Use case to create a new movement."""

    def __init__(
        self,
        repository: IMovementRepository,
        item_repository: IItemRepository,
        warehouse_repository: IWarehouseRepository,
        event_dispatcher: EventDispatcher | None = None,
    ) -> None:
        """Initialize the use case."""

        self._repository = repository
        self._item_repository = item_repository
        self._warehouse_repository = warehouse_repository
        self._event_dispatcher = event_dispatcher

    async def execute(self, request: CreateMovementRequestDTO) -> Movement:
        """Execute the use case."""

        # Verify if item exists
        item = await self._item_repository.get_by_id(request.item_id)
        if item is None:
            raise ItemNotFoundError(f"Item with id {request.item_id} not found.")

        # Verify if warehouse exists
        warehouse = await self._warehouse_repository.get_by_id(request.warehouse_id)
        if warehouse is None:
            raise WarehouseNotFoundError(
                f"Warehouse with id {request.warehouse_id} not found."
            )

        movement = Movement(
            item_id=request.item_id,
            warehouse_id=request.warehouse_id,
            quantity=Quantity(value=request.quantity),
            movement_type=MovementType(request.movement_type),
            occurred_at=request.occurred_at,
        )

        saved_movement = await self._repository.save(movement)

        if self._event_dispatcher:
            for event in movement.list_domain_events():
                await self._event_dispatcher.publish(event)
            movement.clear_domain_events()

        return saved_movement
