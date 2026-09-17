from dataclasses import dataclass
from uuid import UUID

from src.core.domain import DomainEvent
from src.inventory.domain.enums import MovementType


@dataclass(kw_only=True, frozen=True)
class MovementCreatedEvent(DomainEvent):
    """Event published when a new inventory movement occurs."""

    item_id: UUID
    warehouse_id: UUID
    quantity_value: str
    movement_type: MovementType
