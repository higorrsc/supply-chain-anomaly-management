from uuid import uuid4

import pytest

from src.inventory.application.use_cases.commands.update_warehouse import (
    UpdateWarehouseRequestDTO,
    UpdateWarehouseUseCase,
)
from src.inventory.domain.entities import Warehouse
from src.inventory.domain.exceptions import WarehouseNotFoundError
from tests.fakes.repositories import FakeWarehouseRepository


class TestUpdateWarehouseUseCase:
    """Test suite for update warehouse use case."""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully."""

        repo = FakeWarehouseRepository()
        warehouse = Warehouse(
            name="Old Warehouse",
            location_code="BR-RJ",
            is_active=True,
        )
        await repo.save(warehouse)

        use_case = UpdateWarehouseUseCase(repository=repo)
        dto = UpdateWarehouseRequestDTO(
            id=warehouse.id,
            name="New Warehouse",
            location_code="BR-SP",
        )

        result = await use_case.execute(dto)

        assert result is not None
        assert result.id == warehouse.id
        assert result.name == "New Warehouse"
        assert result.location_code == "BR-SP"

        saved_warehouse = await repo.get_by_id(warehouse.id)
        assert saved_warehouse is not None
        assert saved_warehouse.name == "New Warehouse"
        assert saved_warehouse.location_code == "BR-SP"

    async def test_execute_use_case_with_invalid_id_raises_error(self) -> None:
        """Test if updating a warehouse with an invalid id raises an error."""

        repo = FakeWarehouseRepository()
        use_case = UpdateWarehouseUseCase(repository=repo)
        dto = UpdateWarehouseRequestDTO(
            id=uuid4(),
            name="New Warehouse",
            location_code="BR-SP",
        )

        with pytest.raises(WarehouseNotFoundError):
            await use_case.execute(dto)
