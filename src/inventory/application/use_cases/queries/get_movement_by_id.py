from src.core.application.use_cases.queries import GenericGetByIdUseCase
from src.inventory.domain.entities import Movement
from src.inventory.domain.exceptions import MovementNotFoundError
from src.inventory.domain.repositories import IMovementRepository


class GetMovementByIdUseCase(GenericGetByIdUseCase[Movement]):
    """Use case to get a movement by its id."""

    def __init__(self, repository: IMovementRepository) -> None:
        """Initialize the use case."""

        super().__init__(
            repository=repository,
            not_found_exception=MovementNotFoundError,
            not_found_message="Movement with id {id} not found.",
        )
