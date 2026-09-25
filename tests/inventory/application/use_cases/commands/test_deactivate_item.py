from src.core.application.use_cases.commands import DeactivateRequestDTO
from src.inventory.application.use_cases.commands import DeactivateItemUseCase
from src.inventory.domain.entities import Item
from src.inventory.domain.value_objects import SKU
from tests.fakes.repositories import FakeItemRepository


class TestDeactivateItemUseCase:
    """Test suite for deactivate item use case"""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully"""

        repo = FakeItemRepository()
        data = Item(
            sku=SKU(value="SKU-ITEM-132"),
            description="Item To Save",
            is_active=True,
        )

        saved_data = await repo.save(data)
        assert saved_data is not None

        dto = DeactivateRequestDTO(data.id)
        use_case = DeactivateItemUseCase(repository=repo)

        await use_case.execute(dto)

        result = await repo.get_by_id(data.id)
        assert result is not None
        assert result.is_active is False
