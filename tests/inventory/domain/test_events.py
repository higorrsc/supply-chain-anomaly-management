from datetime import UTC, datetime
from uuid import uuid4

from src.inventory.domain.enums import MovementType
from src.inventory.domain.events import MovementCreatedEvent


def test_movement_created_event() -> None:
    movement_id = uuid4()
    item_id = uuid4()
    warehouse_id = uuid4()
    occurrence_date = datetime.now(UTC)

    event = MovementCreatedEvent(
        movement_id=movement_id,
        item_id=item_id,
        warehouse_id=warehouse_id,
        quantity_value="10.5",
        movement_type=MovementType.IN,
        occurrence_date=occurrence_date,
    )

    assert event.movement_id == movement_id
    assert event.item_id == item_id
    assert event.warehouse_id == warehouse_id
    assert event.quantity_value == "10.5"
    assert event.movement_type == MovementType.IN
    assert event.occurrence_date == occurrence_date
