from src.core.application.use_cases.commands import DeleteRequestDTO
from src.inventory.application.use_cases.commands import DeleteItemUseCase
from src.inventory.domain.entities import Item
from src.inventory.domain.value_objects import SKU
from tests.fakes.repositories import FakeItemRepository


class TestDeleteItemUseCase:
    """Test suite for delete item use case"""

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

        dto = DeleteRequestDTO(data.id)
        use_case = DeleteItemUseCase(repository=repo)

        await use_case.execute(dto)

        result = await repo.get_by_id(data.id)
        assert result is None
