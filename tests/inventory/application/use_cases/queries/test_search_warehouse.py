from src.core.application.use_cases.queries import SearchRequestDTO
from src.inventory.application.use_cases.queries.search_warehouse import (
    SearchWarehouseUseCase,
)
from src.inventory.domain.entities import Warehouse
from tests.fakes.repositories import FakeWarehouseRepository


class TestSearchWarehouseUseCase:
    """Test suite for search warehouse use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeWarehouseRepository()

        await repo.save(
            Warehouse(name="Warehouse A", location_code="BR-SP", is_active=True)
        )
        await repo.save(
            Warehouse(name="Warehouse B", location_code="BR-RJ", is_active=True)
        )

        use_case = SearchWarehouseUseCase(repository=repo)
        dto = SearchRequestDTO(filters={})

        result = await use_case.execute(dto)

        assert result is not None
        assert len(result.data) == 2
        assert result.meta.get("total_items") == 2
