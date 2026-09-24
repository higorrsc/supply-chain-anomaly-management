from src.core.application.use_cases.queries import GenericSearchUseCase
from src.inventory.domain.entities import Warehouse
from src.inventory.domain.repositories import IWarehouseRepository


class SearchWarehouseUseCase(GenericSearchUseCase[Warehouse]):
    """Use case to search warehouses."""

    def __init__(self, repository: IWarehouseRepository) -> None:
        """Initialize the use case."""

        super().__init__(repository=repository)
