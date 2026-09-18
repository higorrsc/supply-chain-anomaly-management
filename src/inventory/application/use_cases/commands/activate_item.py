from src.core.application.use_cases.commands import GenericActivateUseCase
from src.inventory.domain.entities import Item
from src.inventory.domain.exceptions import ItemNotFoundError
from src.inventory.domain.repositories import IItemRepository


class ActivateItemUseCase(GenericActivateUseCase[Item]):
    """Use case to activate an item by its id"""

    def __init__(self, repository: IItemRepository) -> None:
        """Initialize the use case"""

        super().__init__(
            repository=repository,
            not_found_exception=ItemNotFoundError,
            not_found_message="Item with id {id} not found.",
        )
