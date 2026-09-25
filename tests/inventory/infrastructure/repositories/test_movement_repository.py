from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.inventory.domain.entities import Item, Movement, Warehouse
from src.inventory.domain.enums import MovementType
from src.inventory.domain.value_objects import SKU, Quantity
from src.inventory.infrastructure.repositories.item_repository import ItemRepository
from src.inventory.infrastructure.repositories.movement_repository import (
    MovementRepository,
)
from src.inventory.infrastructure.repositories.warehouse_repository import (
    WarehouseRepository,
)


class TestMovementRepository:
    """Test suite for MovementRepository using an in-memory database."""

    async def test_save_and_get_by_id(self, db_session: AsyncSession) -> None:
        """Test saving and retrieving a movement."""

        # Setup prerequisites
        item_repo = ItemRepository(session=db_session)
        warehouse_repo = WarehouseRepository(session=db_session)

        item = Item(sku=SKU(value="SKU-MOVS"), description="Mov Item", is_active=True)
        warehouse = Warehouse(name="Mov Warehouse", location_code="BR", is_active=True)

        saved_item = await item_repo.save(item)
        saved_warehouse = await warehouse_repo.save(warehouse)

        movement_repo = MovementRepository(session=db_session)
        movement = Movement(
            item_id=saved_item.id,
            warehouse_id=saved_warehouse.id,
            quantity=Quantity(value=Decimal("50.0")),
            movement_type=MovementType.IN,
            occurred_at=datetime.now(UTC),
        )

        saved_movement = await movement_repo.save(movement)
        assert saved_movement is not None
        assert saved_movement.id is not None
        assert saved_movement.quantity.value == Decimal("50.0")

        retrieved_movement = await movement_repo.get_by_id(saved_movement.id)
        assert retrieved_movement is not None
        assert retrieved_movement.id == saved_movement.id
        assert retrieved_movement.item_id == saved_item.id
        assert retrieved_movement.warehouse_id == saved_warehouse.id
        assert retrieved_movement.quantity.value == Decimal("50.0")

    async def test_delete_movement(self, db_session: AsyncSession) -> None:
        """Test deleting a movement."""

        # Setup prerequisites
        item_repo = ItemRepository(session=db_session)
        warehouse_repo = WarehouseRepository(session=db_session)

        item = Item(sku=SKU(value="SKU-DELS"), description="Del Item", is_active=True)
        warehouse = Warehouse(name="Del Warehouse", location_code="BR", is_active=True)

        saved_item = await item_repo.save(item)
        saved_warehouse = await warehouse_repo.save(warehouse)

        movement_repo = MovementRepository(session=db_session)
        movement = Movement(
            item_id=saved_item.id,
            warehouse_id=saved_warehouse.id,
            quantity=Quantity(value=Decimal("10.0")),
            movement_type=MovementType.OUT,
            occurred_at=datetime.now(UTC),
        )

        saved_movement = await movement_repo.save(movement)
        await movement_repo.delete(saved_movement.id)

        retrieved_movement = await movement_repo.get_by_id(saved_movement.id)
        assert retrieved_movement is None
