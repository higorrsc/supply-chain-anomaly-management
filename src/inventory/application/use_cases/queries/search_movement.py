from src.core.application.use_cases.queries import GenericSearchUseCase
from src.inventory.domain.entities import Movement
from src.inventory.domain.repositories import IMovementRepository


class SearchMovementUseCase(GenericSearchUseCase[Movement]):
    """Use case to search movements."""

    def __init__(self, repository: IMovementRepository) -> None:
        """Initialize the use case."""

        super().__init__(repository=repository)
