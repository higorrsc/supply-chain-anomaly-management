from src.inventory.application.use_cases.commands.create_warehouse import (
    CreateWarehouseRequestDTO,
    CreateWarehouseUseCase,
)
from tests.fakes.repositories import FakeWarehouseRepository


class TestCreateWarehouseUseCase:
    """Test suite for create warehouse use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeWarehouseRepository()
        use_case = CreateWarehouseUseCase(repository=repo)
        dto = CreateWarehouseRequestDTO(name="Main Warehouse", location_code="BR-SP")

        result = await use_case.execute(dto)

        assert result is not None
        assert result.id is not None
        assert result.name == "Main Warehouse"
        assert result.location_code == "BR-SP"
        assert result.is_active is True

        saved_warehouse = await repo.get_by_id(result.id)
        assert saved_warehouse is not None
        assert saved_warehouse == result

    async def test_execute_use_case_with_is_active_false(self) -> None:
        """Test if can create a warehouse with is_active set to False."""

        repo = FakeWarehouseRepository()
        use_case = CreateWarehouseUseCase(repository=repo)
        dto = CreateWarehouseRequestDTO(
            name="Inactive Warehouse", location_code="BR-MG", is_active=False
        )

        result = await use_case.execute(dto)

        assert result is not None
        assert result.is_active is False

        saved_warehouse = await repo.get_by_id(result.id)
        assert saved_warehouse is not None
        assert saved_warehouse.is_active is False
