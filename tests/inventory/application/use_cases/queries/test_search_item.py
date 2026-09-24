from src.core.application.use_cases.queries import SearchRequestDTO
from src.inventory.application.use_cases.queries.search_item import SearchItemUseCase
from src.inventory.domain.entities import Item
from src.inventory.domain.value_objects import SKU
from tests.fakes.repositories import FakeItemRepository


class TestSearchItemUseCase:
    """Test suite for search item use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeItemRepository()

        await repo.save(
            Item(sku=SKU(value="SKU-1111"), description="First Item", is_active=True)
        )
        await repo.save(
            Item(sku=SKU(value="SKU-2222"), description="Second Item", is_active=True)
        )

        use_case = SearchItemUseCase(repository=repo)
        dto = SearchRequestDTO(filters={})

        result = await use_case.execute(dto)

        assert result is not None
        assert len(result.data) == 2
        assert result.meta.get("total_items") == 2
