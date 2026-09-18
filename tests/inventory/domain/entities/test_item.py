import pytest
from faker import Faker

from src.inventory.domain.entities import Item
from src.inventory.domain.exceptions import InvalidItemError
from src.inventory.domain.value_objects import SKU


class TestItem:
    """Test suite for Item entity"""

    def test_can_create_an_item_successfully(self) -> None:
        """Test if can create an item with all attributes"""

        fake = Faker()

        item_id = fake.uuid4(cast_to=None)
        item = Item(
            id=item_id,
            sku=SKU(value="CEL-XIAO-123"),
            description="CELULAR XIAOMI 123",
            is_active=True,
        )

        assert item is not None
        assert item.id == item_id
        assert item.sku.value == "CEL-XIAO-123"
        assert item.is_active is True

    def test_if_can_create_item_without_description_raises_error(self) -> None:
        """Test if can create an item without pass description"""

        with pytest.raises(InvalidItemError) as exc_info:
            Item(
                sku=SKU(value="CEL-XIAO-123"),
                description="",
                is_active=True,
            )

        assert "Description must be a non-empty string." in str(exc_info)

        with pytest.raises(InvalidItemError) as exc_info:
            Item(
                sku=SKU(value="CEL-XIAO-123"),
                description=None,  # type: ignore
                is_active=True,
            )

        assert "Description must be a non-empty string." in str(exc_info)

    def test_activate_and_deactivate_an_item_successfully(self) -> None:
        """Test if can activate and deactivate an Item"""

        fake = Faker()

        item_id = fake.uuid4(cast_to=None)
        item = Item(
            id=item_id,
            sku=SKU(value="CEL-XIAO-123"),
            description="CELULAR XIAOMI 123",
            is_active=False,
        )

        assert item is not None
        assert item.id == item_id
        assert item.sku.value == "CEL-XIAO-123"
        assert item.is_active is False

        item.activate()
        assert item.is_active is True

        item.deactivate()
        assert item.is_active is False

    def test_if_activate_an_active_item_raises_error(self) -> None:
        """Test if try to activate an active item raises error"""

        item = Item(
            sku=SKU(value="CEL-XIAO-123"),
            description="CELULAR XIAOMI 123",
            is_active=True,
        )

        assert item is not None
        assert item.sku.value == "CEL-XIAO-123"
        assert item.is_active is True

        with pytest.raises(InvalidItemError) as exc_info:
            item.activate()

        assert "Item already active." in str(exc_info)

    def test_if_deactivate_an_inactive_item_raises_error(self) -> None:
        """Test if try to deactivate and inactive item raises error"""

        item = Item(
            sku=SKU(value="CEL-XIAO-123"),
            description="CELULAR XIAOMI 123",
            is_active=False,
        )

        assert item is not None
        assert item.sku.value == "CEL-XIAO-123"
        assert item.is_active is False

        with pytest.raises(InvalidItemError) as exc_info:
            item.deactivate()

        assert "Item already inactive." in str(exc_info)
