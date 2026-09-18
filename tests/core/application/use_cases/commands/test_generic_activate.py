import pytest
from faker import Faker

from src.core.application.use_cases.commands import (
    ActivateRequestDTO,
    GenericActivateUseCase,
)
from src.core.domain import EntityNotFoundError, EntityValidationError
from src.core.infrastructure.repository import InMemoryRepository
from tests.fakes import FakeEntity


class TestGenericActivateUseCase:
    """Test suite for generic activate use case"""

    async def test_execute_use_case_successfully(self) -> None:
        """Test if can execute use case successfully"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save", is_active=False)

        saved_data = await repo.save(data)
        assert saved_data is not None

        dto = ActivateRequestDTO(data.id)
        use_case = GenericActivateUseCase(
            repository=repo,
            not_found_exception=EntityNotFoundError,
        )

        await use_case.execute(dto)

        result = await repo.get_by_id(data.id)
        assert result is not None
        assert result.is_active is True

    async def test_execute_use_case_with_invalid_id_raises_error(self) -> None:
        """Test if raises error when execute use case with invalid id"""

        fake = Faker()
        repo = InMemoryRepository[FakeEntity]()

        dto = ActivateRequestDTO(fake.uuid4(cast_to=None))
        with pytest.raises(EntityNotFoundError) as exc_info:
            use_case = GenericActivateUseCase(
                repository=repo,
                not_found_exception=EntityNotFoundError,
            )
            await use_case.execute(dto)

        assert f"Entity with id {dto.id} not found." in str(exc_info)

    async def test_execute_use_case_with_active_entity_raises_error(self) -> None:
        """Test if raises error when execute use case at active entity"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save", is_active=True)

        saved_data = await repo.save(data)
        assert saved_data is not None

        dto = ActivateRequestDTO(data.id)
        with pytest.raises(EntityValidationError) as exc_info:
            use_case = GenericActivateUseCase(
                repository=repo,
                not_found_exception=EntityNotFoundError,
            )
            await use_case.execute(dto)

        assert "Entity already active." in str(exc_info)
