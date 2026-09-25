from src.core.application.use_cases.queries import GetByIdRequestDTO
from src.inventory.application.use_cases.queries import GetItemByIdUseCase
from src.inventory.domain.entities import Item
from src.inventory.domain.value_objects import SKU
from tests.fakes.repositories import FakeItemRepository


class TestGenericGetByIdUseCase:
    """Test suite for generic Get By Id use case"""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully"""

        repo = FakeItemRepository()
        data = Item(
            sku=SKU(value="SKU-ITEM-132"),
            description="Item To Save",
            is_active=False,
        )

        saved_data = await repo.save(data)
        assert saved_data is not None

        dto = GetByIdRequestDTO(data.id)
        use_case = GetItemByIdUseCase(repository=repo)

        result = await use_case.execute(dto)
        assert result is not None
        assert result.id == data.id
