from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest
from faker import Faker

from src.core.domain import EntityValidationError
from src.inventory.domain.entities import Movement
from src.inventory.domain.enums import MovementType
from src.inventory.domain.value_objects import Quantity


class TestMovement:
    """Test suite for movement entity"""

    def test_create_valid_movement(self) -> None:
        """Test if can create a valid movement with data"""

        fake = Faker()

        movement = Movement(
            item_id=fake.uuid4(cast_to=None),
            warehouse_id=fake.uuid4(cast_to=None),
            quantity=Quantity(value=Decimal("1")),
            movement_type=MovementType.ADJ,
            occurred_at=datetime.now(UTC),
        )

        assert movement is not None
        assert isinstance(movement.id, UUID)
        assert len(movement.list_domain_events()) == 1

    def test_movement_with_invalid_item_id_uuid_instance_raises_error(self) -> None:
        """Test if invalid item id raises an exception."""

        fake = Faker()

        with pytest.raises(EntityValidationError) as exc_info:
            Movement(
                item_id="0000-0000",  # type: ignore
                warehouse_id=fake.uuid4(cast_to=None),
                quantity=Quantity(value=Decimal("10.0")),
                movement_type=MovementType.IN,
                occurred_at=datetime.now(None),
            )

        assert "Item ID must be a valid UUID." in str(exc_info.value)

    def test_movement_with_invalid_warehouse_id_uuid_instance_raises_error(
        self,
    ) -> None:
        """Test if invalid warehouse id raises an exception."""

        fake = Faker()

        with pytest.raises(EntityValidationError) as exc_info:
            Movement(
                item_id=fake.uuid4(cast_to=None),
                warehouse_id="0000-0000",  # type: ignore
                quantity=Quantity(value=Decimal("10.0")),
                movement_type=MovementType.IN,
                occurred_at=datetime.now(None),
            )

        assert "Warehouse ID must be a valid UUID." in str(exc_info.value)

    def test_movement_occurrence_date_without_timezone_raises_error(self) -> None:
        """Test if date without timezone raises an exception."""

        fake = Faker()

        with pytest.raises(EntityValidationError) as exc_info:
            Movement(
                item_id=fake.uuid4(cast_to=None),
                warehouse_id=fake.uuid4(cast_to=None),
                quantity=Quantity(value=Decimal("10.0")),
                movement_type=MovementType.IN,
                occurred_at=datetime.now(None),
            )

        assert "Occurrence date must be timezone-aware." in str(exc_info.value)

    def test_movement_occurrence_date_in_future_raises_error(self) -> None:
        """Test if a future date raises an exception."""

        fake = Faker()

        with pytest.raises(EntityValidationError) as exc_info:
            Movement(
                item_id=fake.uuid4(cast_to=None),
                warehouse_id=fake.uuid4(cast_to=None),
                quantity=Quantity(value=Decimal("10.0")),
                movement_type=MovementType.IN,
                occurred_at=fake.future_datetime(tzinfo=UTC),
            )

        assert "Occurrence date cannot be in the future." in str(exc_info.value)
