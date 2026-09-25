from src.core.application.use_cases.commands import GenericActivateUseCase
from src.inventory.domain.entities import Warehouse
from src.inventory.domain.exceptions import WarehouseNotFoundError
from src.inventory.domain.repositories import IWarehouseRepository


class ActivateWarehouseUseCase(GenericActivateUseCase[Warehouse]):
    """Use case to activate an warehouse by its id"""

    def __init__(self, repository: IWarehouseRepository) -> None:
        """Initialize the use case"""

        super().__init__(
            repository=repository,
            not_found_exception=WarehouseNotFoundError,
            not_found_message="Warehouse with id {id} not found.",
        )
