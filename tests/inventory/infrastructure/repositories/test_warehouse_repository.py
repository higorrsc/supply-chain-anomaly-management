from sqlalchemy.ext.asyncio import AsyncSession

from src.inventory.domain.entities import Warehouse
from src.inventory.infrastructure.repositories.warehouse_repository import (
    WarehouseRepository,
)


class TestWarehouseRepository:
    """Test suite for WarehouseRepository using an in-memory database."""

    async def test_save_and_get_by_id(self, db_session: AsyncSession) -> None:
        """Test saving and retrieving a warehouse."""

        repository = WarehouseRepository(session=db_session)
        warehouse = Warehouse(
            name="Main Warehouse", location_code="BR-SP", is_active=True
        )

        saved_warehouse = await repository.save(warehouse)
        assert saved_warehouse is not None
        assert saved_warehouse.id is not None

        retrieved_warehouse = await repository.get_by_id(saved_warehouse.id)
        assert retrieved_warehouse is not None
        assert retrieved_warehouse.id == saved_warehouse.id
        assert retrieved_warehouse.name == "Main Warehouse"
        assert retrieved_warehouse.location_code == "BR-SP"

    async def test_update_warehouse(self, db_session: AsyncSession) -> None:
        """Test updating an existing warehouse."""

        repository = WarehouseRepository(session=db_session)
        warehouse = Warehouse(name="Old Name", location_code="OLD", is_active=True)
        saved_warehouse = await repository.save(warehouse)

        saved_warehouse.name = "New Name"
        updated_warehouse = await repository.update(saved_warehouse)

        assert updated_warehouse.name == "New Name"

        retrieved_warehouse = await repository.get_by_id(saved_warehouse.id)
        assert retrieved_warehouse is not None
        assert retrieved_warehouse.name == "New Name"

    async def test_delete_warehouse(self, db_session: AsyncSession) -> None:
        """Test deleting a warehouse."""

        repository = WarehouseRepository(session=db_session)
        warehouse = Warehouse(name="To Delete", location_code="DEL", is_active=True)
        saved_warehouse = await repository.save(warehouse)

        await repository.delete(saved_warehouse.id)

        retrieved_warehouse = await repository.get_by_id(saved_warehouse.id)
        assert retrieved_warehouse is None
