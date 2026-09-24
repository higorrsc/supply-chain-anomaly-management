import pytest

from src.core.domain import ConflictError
from src.inventory.application.use_cases.commands.create_item import (
    CreateItemRequestDTO,
    CreateItemUseCase,
)
from src.inventory.domain.entities import Item
from src.inventory.domain.value_objects import SKU
from tests.fakes.repositories import FakeItemRepository


class TestCreateItemUseCase:
    """Test suite for create item use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeItemRepository()
        use_case = CreateItemUseCase(repository=repo)
        dto = CreateItemRequestDTO(sku="SKU-1234", description="Test Item")

        result = await use_case.execute(dto)

        assert result is not None
        assert result.id is not None
        assert result.sku.value == "SKU-1234"
        assert result.description == "Test Item"
        assert result.is_active is True

        saved_item = await repo.get_by_id(result.id)
        assert saved_item is not None
        assert saved_item == result

    async def test_execute_use_case_with_duplicate_sku_raises_error(self) -> None:
        """Test if creating an item with a duplicate sku raises an error."""

        repo = FakeItemRepository()
        existing_item = Item(
            sku=SKU(value="SKU-1234"),
            description="Existing Item",
            is_active=True,
        )
        await repo.save(existing_item)

        use_case = CreateItemUseCase(repository=repo)
        dto = CreateItemRequestDTO(sku="SKU-1234", description="Another Item")

        with pytest.raises(ConflictError):
            await use_case.execute(dto)

    async def test_execute_use_case_with_is_active_false(self) -> None:
        """Test if can create an item with is_active set to False."""

        repo = FakeItemRepository()
        use_case = CreateItemUseCase(repository=repo)
        dto = CreateItemRequestDTO(
            sku="SKU-INACTIVE", description="Inactive", is_active=False
        )

        result = await use_case.execute(dto)

        assert result is not None
        assert result.is_active is False

        saved_item = await repo.get_by_id(result.id)
        assert saved_item is not None
        assert saved_item.is_active is False
