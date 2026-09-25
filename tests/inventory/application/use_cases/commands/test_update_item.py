from uuid import uuid4

import pytest

from src.inventory.application.use_cases.commands.update_item import (
    UpdateItemRequestDTO,
    UpdateItemUseCase,
)
from src.inventory.domain.entities import Item
from src.inventory.domain.exceptions import ItemNotFoundError
from src.inventory.domain.value_objects import SKU
from tests.fakes.repositories import FakeItemRepository


class TestUpdateItemUseCase:
    """Test suite for update item use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeItemRepository()
        item = Item(
            sku=SKU(value="SKU-1234"),
            description="Old Description",
            is_active=True,
        )
        await repo.save(item)

        use_case = UpdateItemUseCase(repository=repo)
        dto = UpdateItemRequestDTO(id=item.id, description="New Description")

        result = await use_case.execute(dto)

        assert result is not None
        assert result.id == item.id
        assert result.description == "New Description"

        saved_item = await repo.get_by_id(item.id)
        assert saved_item is not None
        assert saved_item.description == "New Description"

    async def test_execute_use_case_with_invalid_id_raises_error(self) -> None:
        """Test if updating an item with an invalid id raises an error."""

        repo = FakeItemRepository()
        use_case = UpdateItemUseCase(repository=repo)
        dto = UpdateItemRequestDTO(id=uuid4(), description="New Description")

        with pytest.raises(ItemNotFoundError):
            await use_case.execute(dto)
