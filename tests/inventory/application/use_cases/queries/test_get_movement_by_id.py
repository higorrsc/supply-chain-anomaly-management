from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.core.application.use_cases.queries import GetByIdRequestDTO
from src.inventory.application.use_cases.queries.get_movement_by_id import (
    GetMovementByIdUseCase,
)
from src.inventory.domain.entities import Movement
from src.inventory.domain.enums import MovementType
from src.inventory.domain.exceptions import MovementNotFoundError
from src.inventory.domain.value_objects import Quantity
from tests.fakes.repositories import FakeMovementRepository


class TestGetMovementByIdUseCase:
    """Test suite for get movement by id use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeMovementRepository()

        movement = Movement(
            item_id=uuid4(),
            warehouse_id=uuid4(),
            quantity=Quantity(value=Decimal("10.0")),
            movement_type=MovementType.IN,
            occurred_at=datetime.now(UTC),
        )
        await repo.save(movement)

        use_case = GetMovementByIdUseCase(repository=repo)
        dto = GetByIdRequestDTO(id=movement.id)

        result = await use_case.execute(dto)

        assert result is not None
        assert result.id == movement.id
        assert result.item_id == movement.item_id

    async def test_execute_use_case_with_invalid_id_raises_error(self) -> None:
        """Test if getting a non-existent movement raises an error."""

        repo = FakeMovementRepository()
        use_case = GetMovementByIdUseCase(repository=repo)
        dto = GetByIdRequestDTO(id=uuid4())

        with pytest.raises(MovementNotFoundError):
            await use_case.execute(dto)
