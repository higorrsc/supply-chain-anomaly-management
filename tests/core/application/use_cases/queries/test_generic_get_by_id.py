import pytest
from faker import Faker

from src.core.application.use_cases.queries import (
    GenericGetByIdUseCase,
    GetByIdRequestDTO,
)
from src.core.domain import EntityNotFoundError
from src.core.infrastructure.repositories import InMemoryRepository
from tests.fakes.entity import FakeEntity


class TestGenericGetByIdUseCase:
    """Test suite for generic Get By Id use case"""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save")

        saved_data = await repo.save(data)
        assert saved_data is not None

        dto = GetByIdRequestDTO(data.id)
        use_case = GenericGetByIdUseCase(
            repository=repo,
            not_found_exception=EntityNotFoundError,
        )

        await use_case.execute(dto)

        result = await repo.get_by_id(data.id)
        assert result is not None
        assert result.id == data.id

    async def test_execute_use_case_with_invalid_id_raises_error(self) -> None:
        """Test if raises error when execute use case with invalid id"""

        fake = Faker()
        repo = InMemoryRepository[FakeEntity]()

        dto = GetByIdRequestDTO(fake.uuid4(cast_to=None))
        with pytest.raises(EntityNotFoundError) as exc_info:
            use_case = GenericGetByIdUseCase(
                repository=repo,
                not_found_exception=EntityNotFoundError,
            )
            await use_case.execute(dto)

        assert f"Entity with id {dto.id} not found." in str(exc_info)
