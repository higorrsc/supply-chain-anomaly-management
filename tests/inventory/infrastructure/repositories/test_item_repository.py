from sqlalchemy.ext.asyncio import AsyncSession

from src.inventory.domain.entities import Item
from src.inventory.domain.value_objects import SKU
from src.inventory.infrastructure.repositories.item_repository import ItemRepository


class TestItemRepository:
    """Test suite for ItemRepository using an in-memory database."""

    async def test_save_and_get_by_id(self, db_session: AsyncSession) -> None:
        """Test saving and retrieving an item."""

        repository = ItemRepository(session=db_session)
        item = Item(sku=SKU(value="SKU-12345"), description="Test Item", is_active=True)

        saved_item = await repository.save(item)
        assert saved_item is not None
        assert saved_item.id is not None
        assert saved_item.sku.value == "SKU-12345"

        retrieved_item = await repository.get_by_id(saved_item.id)
        assert retrieved_item is not None
        assert retrieved_item.id == saved_item.id
        assert retrieved_item.description == "Test Item"

    async def test_get_by_sku(self, db_session: AsyncSession) -> None:
        """Test retrieving an item by SKU."""

        repository = ItemRepository(session=db_session)
        sku = SKU(value="SKU-99999")
        item = Item(sku=sku, description="Unique SKU Item", is_active=True)

        await repository.save(item)

        retrieved_item = await repository.get_by_sku(sku)
        assert retrieved_item is not None
        assert retrieved_item.sku.value == "SKU-99999"

    async def test_update_item(self, db_session: AsyncSession) -> None:
        """Test updating an existing item."""

        repository = ItemRepository(session=db_session)
        item = Item(
            sku=SKU(value="SKU-11111"), description="Old Description", is_active=True
        )
        saved_item = await repository.save(item)

        saved_item.description = "New Description"
        saved_item.is_active = False

        updated_item = await repository.update(saved_item)
        assert updated_item.description == "New Description"
        assert updated_item.is_active is False

        retrieved_item = await repository.get_by_id(saved_item.id)
        assert retrieved_item is not None
        assert retrieved_item.description == "New Description"
        assert retrieved_item.is_active is False

    async def test_delete_item(self, db_session: AsyncSession) -> None:
        """Test deleting an item."""

        repository = ItemRepository(session=db_session)
        item = Item(sku=SKU(value="SKU-22222"), description="To Delete", is_active=True)
        saved_item = await repository.save(item)

        await repository.delete(saved_item.id)

        retrieved_item = await repository.get_by_id(saved_item.id)
        assert retrieved_item is None
