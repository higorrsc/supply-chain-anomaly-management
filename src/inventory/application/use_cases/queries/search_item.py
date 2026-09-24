from src.core.application.use_cases.queries import GenericSearchUseCase
from src.inventory.domain.entities import Item
from src.inventory.domain.repositories import IItemRepository


class SearchItemUseCase(GenericSearchUseCase[Item]):
    """Use case to search items."""

    def __init__(self, repository: IItemRepository) -> None:
        """Initialize the use case."""

        super().__init__(repository=repository)
