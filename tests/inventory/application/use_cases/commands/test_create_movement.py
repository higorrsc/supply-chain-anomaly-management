from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.inventory.application.use_cases.commands.create_movement import (
    CreateMovementRequestDTO,
    CreateMovementUseCase,
)
from src.inventory.domain.entities import Item, Warehouse
from src.inventory.domain.enums import MovementType
from src.inventory.domain.exceptions import ItemNotFoundError, WarehouseNotFoundError
from src.inventory.domain.value_objects import SKU
from tests.fakes.repositories import (
    FakeItemRepository,
    FakeMovementRepository,
    FakeWarehouseRepository,
)


class TestCreateMovementUseCase:
    """Test suite for create movement use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeMovementRepository()
        item_repo = FakeItemRepository()
        warehouse_repo = FakeWarehouseRepository()

        # Create prerequisites
        item = Item(sku=SKU(value="SKU-12345"), description="Item", is_active=True)
        await item_repo.save(item)

        warehouse = Warehouse(name="Warehouse", location_code="BR", is_active=True)
        await warehouse_repo.save(warehouse)

        use_case = CreateMovementUseCase(
            repository=repo,
            item_repository=item_repo,
            warehouse_repository=warehouse_repo,
        )

        dto = CreateMovementRequestDTO(
            item_id=item.id,
            warehouse_id=warehouse.id,
            quantity=Decimal("100.5"),
            movement_type=MovementType.IN,
            occurred_at=datetime.now(UTC),
        )

        result = await use_case.execute(dto)

        assert result is not None
        assert result.id is not None
        assert result.item_id == item.id
        assert result.warehouse_id == warehouse.id
        assert result.quantity.value == Decimal("100.5")
        assert result.movement_type == MovementType.IN

        saved_movement = await repo.get_by_id(result.id)
        assert saved_movement is not None
        assert saved_movement == result

    async def test_execute_use_case_with_invalid_item_raises_error(self) -> None:
        """Test if creating a movement with an invalid item id raises an error."""

        repo = FakeMovementRepository()
        item_repo = FakeItemRepository()
        warehouse_repo = FakeWarehouseRepository()

        warehouse = Warehouse(name="Warehouse", location_code="BR", is_active=True)
        await warehouse_repo.save(warehouse)

        use_case = CreateMovementUseCase(
            repository=repo,
            item_repository=item_repo,
            warehouse_repository=warehouse_repo,
        )

        dto = CreateMovementRequestDTO(
            item_id=uuid4(),
            warehouse_id=warehouse.id,
            quantity=Decimal("10.0"),
            movement_type=MovementType.OUT,
            occurred_at=datetime.now(UTC),
        )

        with pytest.raises(ItemNotFoundError):
            await use_case.execute(dto)

    async def test_execute_use_case_with_invalid_warehouse_raises_error(self) -> None:
        """Test if creating a movement with an invalid warehouse id raises an error."""

        repo = FakeMovementRepository()
        item_repo = FakeItemRepository()
        warehouse_repo = FakeWarehouseRepository()

        item = Item(sku=SKU(value="SKU-12345"), description="Item", is_active=True)
        await item_repo.save(item)

        use_case = CreateMovementUseCase(
            repository=repo,
            item_repository=item_repo,
            warehouse_repository=warehouse_repo,
        )

        dto = CreateMovementRequestDTO(
            item_id=item.id,
            warehouse_id=uuid4(),
            quantity=Decimal("10.0"),
            movement_type=MovementType.OUT,
            occurred_at=datetime.now(UTC),
        )

        with pytest.raises(WarehouseNotFoundError):
            await use_case.execute(dto)
