from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from src.core.application.use_cases.queries import SearchRequestDTO
from src.inventory.application.use_cases.queries.search_movement import (
    SearchMovementUseCase,
)
from src.inventory.domain.entities import Movement
from src.inventory.domain.enums import MovementType
from src.inventory.domain.value_objects import Quantity
from tests.fakes.repositories import FakeMovementRepository


class TestSearchMovementUseCase:
    """Test suite for search movement use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeMovementRepository()

        await repo.save(
            Movement(
                item_id=uuid4(),
                warehouse_id=uuid4(),
                quantity=Quantity(value=Decimal("10.0")),
                movement_type=MovementType.IN,
                occurred_at=datetime.now(UTC),
            )
        )
        await repo.save(
            Movement(
                item_id=uuid4(),
                warehouse_id=uuid4(),
                quantity=Quantity(value=Decimal("5.0")),
                movement_type=MovementType.OUT,
                occurred_at=datetime.now(UTC),
            )
        )

        use_case = SearchMovementUseCase(repository=repo)
        dto = SearchRequestDTO(filters={})

        result = await use_case.execute(dto)

        assert result is not None
        assert len(result.data) == 2
        assert result.meta.get("total_items") == 2
