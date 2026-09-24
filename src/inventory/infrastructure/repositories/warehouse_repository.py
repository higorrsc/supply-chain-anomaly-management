from src.core.infrastructure.repositories.sqlalchemy_repository import (
    SqlAlchemyRepository,
)
from src.inventory.domain.entities import Warehouse
from src.inventory.domain.repositories import IWarehouseRepository
from src.inventory.infrastructure.mappers import WarehouseMapper
from src.inventory.infrastructure.models import WarehouseModel


class WarehouseRepository(
    SqlAlchemyRepository[Warehouse, WarehouseModel],
    IWarehouseRepository,
):
    """Physical repository for Warehouse."""

    @property
    def model_class(self) -> type[WarehouseModel]:
        return WarehouseModel

    def _to_entity(self, model: WarehouseModel) -> Warehouse:
        return WarehouseMapper.to_entity(model)

    def _to_model(self, entity: Warehouse) -> WarehouseModel:
        return WarehouseMapper.to_model(entity)

    def _update_model(self, model: WarehouseModel, entity: Warehouse) -> WarehouseModel:
        return WarehouseMapper.update_model(model, entity)
