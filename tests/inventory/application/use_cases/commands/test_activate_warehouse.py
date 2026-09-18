from src.core.application.use_cases.commands import ActivateRequestDTO
from src.inventory.application.use_cases.commands import ActivateWarehouseUseCase
from src.inventory.domain.entities import Warehouse
from tests.fakes.repositories import FakeWarehouseRepository


class TestActivateWarehouseUseCase:
    """Test suite for activate warehouse use case"""

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

        dto = ActivateRequestDTO(data.id)
        use_case = ActivateWarehouseUseCase(repository=repo)

        await use_case.execute(dto)

        result = await repo.get_by_id(data.id)
        assert result is not None
        assert result.is_active is True
