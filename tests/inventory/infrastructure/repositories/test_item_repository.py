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

    async def test_search_item(self, db_session: AsyncSession) -> None:
        """Test searching items."""
        from src.core.domain import PageRequest, SearchCriteria

        repository = ItemRepository(session=db_session)
        item1 = Item(
            sku=SKU(value="SKU-SEARCH-1"),
            description="Mouse pad",
            is_active=True,
        )
        item2 = Item(
            sku=SKU(value="SKU-SEARCH-2"),
            description="Keyboard",
            is_active=False,
        )
        item3 = Item(
            sku=SKU(value="SKU-SEARCH-3"),
            description="Wireless Mouse",
            is_active=True,
        )

        await repository.save(item1)
        await repository.save(item2)
        await repository.save(item3)

        # Test partial match on description (ILIKE)
        criteria = SearchCriteria(
            filters={"description": "mouse"},
            pagination=PageRequest(page=1, page_size=10),
        )
        result = await repository.search(criteria)
        assert result.total_items >= 2
        assert any(i.sku.value == "SKU-SEARCH-1" for i in result.items)
        assert any(i.sku.value == "SKU-SEARCH-3" for i in result.items)

        # Test exact match on is_active
        criteria = SearchCriteria(
            filters={"is_active": False}, pagination=PageRequest(page=1, page_size=10)
        )
        result = await repository.search(criteria)
        assert any(i.sku.value == "SKU-SEARCH-2" for i in result.items)

    async def test_update_item_not_found(self, db_session: AsyncSession) -> None:
        """Test updating an item that does not exist raises EntityNotFoundError."""
        import pytest

        from src.core.domain import EntityNotFoundError

        repository = ItemRepository(session=db_session)
        item = Item(
            sku=SKU(value="SKU-NONE"),
            description="None",
            is_active=True,
        )

        with pytest.raises(EntityNotFoundError):
            await repository.update(item)
