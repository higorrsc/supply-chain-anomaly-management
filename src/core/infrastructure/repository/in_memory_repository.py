from uuid import UUID

from src.core.domain import (
    AbstractEntity,
    AbstractRepository,
    EntityNotFoundError,
    Page,
    SearchCriteria,
)


class InMemoryRepository[T: AbstractEntity](AbstractRepository[T]):
    """Generic in-memory repository for fast unit testing."""

    def __init__(self) -> None:
        self._data: dict[UUID, T] = {}

    async def save(self, entity: T) -> T:
        """Save an entity to the repository."""

        self._data[entity.id] = entity
        return entity

    async def get_by_id(self, entity_id: UUID) -> T | None:
        """Retrieve an entity by its ID."""

        return self._data.get(entity_id)

    async def update(self, entity: T) -> T:
        """Update an existing entity in the repository."""

        if entity.id not in self._data:
            raise EntityNotFoundError(f"Entity {entity.id} not found.")

        self._data[entity.id] = entity
        return entity

    async def delete(self, entity_id: UUID) -> None:
        """Delete an entity from the repository."""

        if entity_id in self._data:
            del self._data[entity_id]

    async def search(self, criteria: SearchCriteria) -> Page[T]:
        """Search for entities based on criteria, with sorting and pagination."""

        # Implementação simplificada para testes
        items = list(self._data.values())
        return Page(
            items=items,
            total_items=len(items),
            page=criteria.pagination.page,
            page_size=criteria.pagination.page_size,
        )
