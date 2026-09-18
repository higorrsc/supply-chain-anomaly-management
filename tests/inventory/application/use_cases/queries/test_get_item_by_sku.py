import pytest

from src.inventory.application.use_cases.queries import (
    GetItemBySKURequestDTO,
    GetItemBySKUUseCase,
)
from src.inventory.domain.entities import Item
from src.inventory.domain.exceptions import ItemNotFoundError
from src.inventory.domain.value_objects import SKU
from tests.fakes.repositories import FakeItemRepository


class TestGenericGetBySKUUseCase:
    """Test suite for generic Get By Id use case"""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully"""

        repo = FakeItemRepository()
        data = Item(
            sku=SKU(value="SKU-ITEM-132"),
            description="Item To Save",
            is_active=False,
        )

        saved_data = await repo.save(data)
        assert saved_data is not None

        dto = GetItemBySKURequestDTO(data.sku)
        use_case = GetItemBySKUUseCase(
            repository=repo,
            not_found_exception=ItemNotFoundError,
        )

        result = await use_case.execute(dto)
        assert result is not None
        assert result.id == data.id
        assert result.sku == data.sku

    async def test_execute_use_case_with_invalid_sku_raises_error(self) -> None:
        """Test if raises error when execute use case with invalid sku"""

        repo = FakeItemRepository()
        dto = GetItemBySKURequestDTO(SKU(value="SKU-INVALID"))
        with pytest.raises(ItemNotFoundError) as exc_info:
            use_case = GetItemBySKUUseCase(
                repository=repo,
                not_found_exception=ItemNotFoundError,
            )
            await use_case.execute(dto)

        assert f"Item with SKU {dto.sku} not found." in str(exc_info)
