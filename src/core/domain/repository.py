from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class PageRequest:
    """Pagination request."""

    page: int = 1
    page_size: int = 10


@dataclass(frozen=True)
class Page[T]:
    """Paginated collection."""

    items: list[T]
    total_items: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        """Return the total number of pages."""

        if self.total_items == 0:
            return 0

        return (self.total_items + self.page_size - 1) // self.page_size


@dataclass(frozen=True)
class SearchCriteria:
    """Criteria used to search entities."""

    filters: dict[str, Any]
    pagination: PageRequest


class AbstractRepository[T](ABC):
    """Abstract base class for a repository that handles entities of type T."""

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save an entity to the repository."""

        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> T | None:
        """Retrieve an entity by its ID."""

        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update an existing entity in the repository."""

        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> None:
        """Delete an entity from the repository."""

        raise NotImplementedError

    @abstractmethod
    async def search(self, criteria: SearchCriteria) -> Page[T]:
        """Search for entities based on criteria, with sorting and pagination."""

        raise NotImplementedError
