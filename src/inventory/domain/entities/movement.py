from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from src.core.domain import AbstractEntity
from src.inventory.domain.enums import MovementType
from src.inventory.domain.events import MovementCreatedEvent
from src.inventory.domain.exceptions import InvalidMovementError
from src.inventory.domain.value_objects import Quantity


@dataclass(kw_only=True, eq=False, repr=False)
class Movement(AbstractEntity):
    """Class representing an inventory movement"""

    item_id: UUID
    warehouse_id: UUID
    quantity: Quantity
    movement_type: MovementType
    occurred_at: datetime

    def validate(self) -> None:
        """Validate movement creation"""

        if not isinstance(self.item_id, UUID):
            raise InvalidMovementError("Item ID must be a valid UUID.")

        if not isinstance(self.warehouse_id, UUID):
            raise InvalidMovementError("Warehouse ID must be a valid UUID.")

        if self.occurred_at.tzinfo is None:
            raise InvalidMovementError("Occurrence date must be timezone-aware.")

        now = datetime.now(UTC)
        if self.occurred_at > now:
            raise InvalidMovementError("Occurrence date cannot be in the future.")

    def __post_init__(self) -> None:
        """Validate and register domain events after initialization."""

        super().__post_init__()

        event = MovementCreatedEvent(
            item_id=self.item_id,
            warehouse_id=self.warehouse_id,
            quantity_value=str(self.quantity.value),
            movement_type=self.movement_type,
            movement_id=self.id,
            occurrence_date=self.occurred_at,
        )

        self.add_domain_event(event)
