from abc import abstractmethod
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain import (
    AbstractEntity,
    AbstractRepository,
    EntityNotFoundError,
    Page,
    SearchCriteria,
)
from src.core.infrastructure.database.base import Base


class SqlAlchemyRepository[T: AbstractEntity, M: Base](AbstractRepository[T]):
    """Generic physical repository using SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with a database session."""
        self._session = session

    @property
    @abstractmethod
    def model_class(self) -> type[M]:
        """Return the SQLAlchemy model class."""
        raise NotImplementedError

    @abstractmethod
    def _to_entity(self, model: M) -> T:
        """Convert ORM model to Domain Entity."""
        raise NotImplementedError

    @abstractmethod
    def _to_model(self, entity: T) -> M:
        """Convert Domain Entity to ORM model."""
        raise NotImplementedError

    @abstractmethod
    def _update_model(self, model: M, entity: T) -> M:
        """Update ORM model from Domain Entity."""
        raise NotImplementedError

    async def save(self, entity: T) -> T:
        """Save an entity to the repository."""
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, entity_id: UUID) -> T | None:
        """Retrieve an entity by its ID."""
        stmt = select(self.model_class).where(self.model_class.id == entity_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_entity(model)

    async def update(self, entity: T) -> T:
        """Update an existing entity in the repository."""
        stmt = select(self.model_class).where(self.model_class.id == entity.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise EntityNotFoundError(f"Entity {entity.id} not found.")

        updated_model = self._update_model(model, entity)
        await self._session.flush()
        return self._to_entity(updated_model)

    async def delete(self, entity_id: UUID) -> None:
        """Delete an entity from the repository."""
        stmt = delete(self.model_class).where(self.model_class.id == entity_id)
        await self._session.execute(stmt)
        await self._session.flush()

    async def search(self, criteria: SearchCriteria) -> Page[T]:
        """Search for entities based on criteria, with sorting and pagination."""

        stmt = select(self.model_class)

        from sqlalchemy import String

        # Apply exact-match or partial filters if they map directly to column names
        for key, value in criteria.filters.items():
            if hasattr(self.model_class, key):
                column = getattr(self.model_class, key)
                if isinstance(value, str) and isinstance(column.type, String):
                    stmt = stmt.where(column.ilike(f"%{value}%"))
                else:
                    stmt = stmt.where(column == value)

        # Calculate offset
        page = criteria.pagination.page
        page_size = criteria.pagination.page_size
        offset = (page - 1) * page_size

        # We need total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_items_result = await self._session.execute(count_stmt)
        total_items = total_items_result.scalar_one()

        # Apply pagination
        stmt = stmt.offset(offset).limit(page_size)
        result = await self._session.execute(stmt)
        models: Sequence[M] = result.scalars().all()

        return Page(
            items=[self._to_entity(model) for model in models],
            total_items=total_items,
            page=page,
            page_size=page_size,
        )
