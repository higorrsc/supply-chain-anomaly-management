from dataclasses import dataclass
from uuid import UUID

from src.core.domain import AbstractRepository


@dataclass(frozen=True)
class GetByIdRequestDTO:
    """Data Transfer Object for get by id requests."""

    id: UUID


class GenericGetByIdUseCase[T]:
    """Use case for get an entity of type T by Id"""

    def __init__(
        self,
        repository: AbstractRepository[T],
        not_found_exception: type[Exception],
        not_found_message: str = "Entity with id {id} not found.",
    ) -> None:
        """Initialize the delete use case"""

        self._repository = repository
        self._not_found_exception = not_found_exception
        self._not_found_message = not_found_message

    async def execute(self, request: GetByIdRequestDTO) -> T:
        """Execute the use case"""

        entity = await self._repository.get_by_id(entity_id=request.id)
        if entity is None:
            raise self._not_found_exception(
                self._not_found_message.format(id=request.id)
            )

        return entity
