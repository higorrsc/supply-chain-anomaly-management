import pytest

from src.core.domain import EntityNotFoundError, PageRequest, SearchCriteria
from src.core.infrastructure.repositories import InMemoryRepository
from tests.fakes import FakeEntity


class TestInMemoryRepository:
    """Test suite for in-memory repository"""

    def test_can_create_in_memory_repository(self) -> None:
        """Test if can create in-memory repository"""

        repo = InMemoryRepository[FakeEntity]()

        assert repo is not None

    async def test_can_save_data_at_repository(self) -> None:
        """Test if can save data at in-memory repository"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save")

        saved_data = await repo.save(data)

        assert saved_data is not None

    async def test_can_retrieve_data_from_repository_by_id(self) -> None:
        """Test if can retrieve data from in-memory repository by its ID"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save")

        saved_data = await repo.save(data)
        assert saved_data is not None

        retrieved_data = await repo.get_by_id(saved_data.id)
        assert retrieved_data is not None

        assert retrieved_data == saved_data

    async def test_can_update_data_at_repository(self) -> None:
        """Test if can update data from in-memory repository"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save")

        saved_data = await repo.save(data)
        assert saved_data is not None

        data.description = "Updated description"

        updated_data = await repo.update(data)
        assert updated_data is not None

        assert updated_data == saved_data
        assert updated_data.description == "Updated description"

    async def test_update_invalid_entity_raises_error(self) -> None:
        """Test if raises error when update an invalid entity"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save")

        saved_data = await repo.save(data)
        assert saved_data is not None

        other_data = FakeEntity(description="Fake data to save again")

        with pytest.raises(EntityNotFoundError) as exc_info:
            await repo.update(other_data)

        assert f"Entity {other_data.id!s} not found." in str(exc_info)

    async def test_can_delete_data_at_repository(self) -> None:
        """Test if can delete entity"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save")

        saved_data = await repo.save(data)
        assert saved_data is not None

        await repo.delete(saved_data.id)

        retrieved_data = await repo.get_by_id(saved_data.id)
        assert retrieved_data is None

    async def test_can_search_data_at_repository(self) -> None:
        """Test if can search data at repository"""

        repo = InMemoryRepository[FakeEntity]()
        data = FakeEntity(description="Fake data to save")

        saved_data = await repo.save(data)
        assert saved_data is not None

        criteria = SearchCriteria(filters={}, pagination=PageRequest())

        result = await repo.search(criteria)

        assert result is not None
        assert result.total_items == 1
        assert saved_data.id == result.items[0].id
        assert result.total_pages == 1

    async def test_can_search_data_at_empty_repository(self) -> None:
        """Test if can search data at empty repository"""

        repo = InMemoryRepository[FakeEntity]()
        criteria = SearchCriteria(filters={}, pagination=PageRequest())

        result = await repo.search(criteria)

        assert result is not None
        assert result.total_items == 0
        assert result.total_pages == 0
