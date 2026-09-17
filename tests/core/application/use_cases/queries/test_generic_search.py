from src.core.application.use_cases.queries import (
    GenericSearchUseCase,
    SearchRequestDTO,
)
from src.core.infrastructure.repository import InMemoryRepository
from tests.fakes.entity import FakeEntity


class TestGenericSearchUseCase:
    """Test suite for generic search use case"""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully"""

        repo = InMemoryRepository[FakeEntity]()

        saved_data = await repo.save(FakeEntity(description="Fake data to save"))
        assert saved_data is not None

        another_data = await repo.save(
            FakeEntity(description="Another Fake data to save")
        )
        assert another_data is not None

        use_case = GenericSearchUseCase(repo)
        result = await use_case.execute(
            SearchRequestDTO(filters={"description": "fake data"})
        )

        assert result is not None, result.data
        assert len(result.data) == 2
        assert result.meta.get("total_items") == 2
