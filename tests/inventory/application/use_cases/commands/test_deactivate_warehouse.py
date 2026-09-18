from src.core.application.use_cases.commands import DeactivateRequestDTO
from src.inventory.application.use_cases.commands import DeactivateWarehouseUseCase
from src.inventory.domain.entities import Warehouse
from tests.fakes.repositories import FakeWarehouseRepository


class TestDeactivateWarehouseUseCase:
    """Test suite for deactivate warehouse use case"""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully"""

        repo = FakeWarehouseRepository()
        data = Warehouse(
            name="Warehouse 001 DF",
            location_code="DF-001-WH",
            is_active=True,
        )

        saved_data = await repo.save(data)
        assert saved_data is not None

        dto = DeactivateRequestDTO(data.id)
        use_case = DeactivateWarehouseUseCase(repository=repo)

        await use_case.execute(dto)

        result = await repo.get_by_id(data.id)
        assert result is not None
        assert result.is_active is False
