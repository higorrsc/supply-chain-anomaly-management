from src.core.application.use_cases.queries import GetByIdRequestDTO
from src.inventory.application.use_cases.queries import GetWarehouseByIdUseCase
from src.inventory.domain.entities import Warehouse
from tests.fakes.repositories import FakeWarehouseRepository


class TestGenericGetByIdUseCase:
    """Test suite for generic Get By Id use case"""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully"""

        repo = FakeWarehouseRepository()
        data = Warehouse(
            name="Warehouse 001 DF",
            location_code="DF-001-WH",
            is_active=False,
        )

        saved_data = await repo.save(data)
        assert saved_data is not None

        dto = GetByIdRequestDTO(data.id)
        use_case = GetWarehouseByIdUseCase(repository=repo)

        result = await use_case.execute(dto)
        assert result is not None
        assert result.id == data.id
