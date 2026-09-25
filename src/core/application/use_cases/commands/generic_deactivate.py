from dataclasses import dataclass
from uuid import UUID

from src.core.domain import AbstractRepository, ActivatableEntity


@dataclass(frozen=True)
class DeactivateRequestDTO:
    """Data Transfer Object for deactivate requests."""

    id: UUID


class GenericDeactivateUseCase[T: ActivatableEntity]:
    """Use case for deactivating an entity of type T"""

    def __init__(
        self,
        repository: AbstractRepository[T],
        not_found_exception: type[Exception],
        not_found_message: str = "Entity with id {id} not found.",
    ) -> None:
        """Initialize the deactivate use case"""

        self._repository = repository
        self._not_found_exception = not_found_exception
        self._not_found_message = not_found_message

    async def execute(self, request: DeactivateRequestDTO) -> None:
        """Execute the use case"""

        entity = await self._repository.get_by_id(entity_id=request.id)
        if entity is None:
            raise self._not_found_exception(
                self._not_found_message.format(id=request.id)
            )

        entity.deactivate()
        await self._repository.update(entity=entity)
