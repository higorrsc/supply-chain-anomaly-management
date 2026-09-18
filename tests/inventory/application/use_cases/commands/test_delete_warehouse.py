from src.core.application.use_cases.commands import DeleteRequestDTO
from src.inventory.application.use_cases.commands import DeleteWarehouseUseCase
from src.inventory.domain.entities import Warehouse
from tests.fakes.repositories import FakeWarehouseRepository


class TestDeleteWarehouseUseCase:
    """Test suite for delete warehouse use case"""

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

        dto = DeleteRequestDTO(data.id)
        use_case = DeleteWarehouseUseCase(repository=repo)

        await use_case.execute(dto)

        result = await repo.get_by_id(data.id)
        assert result is None
