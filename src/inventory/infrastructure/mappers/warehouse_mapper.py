from src.inventory.domain.entities import Warehouse
from src.inventory.infrastructure.models import WarehouseModel


class WarehouseMapper:
    """Mapper for Warehouse entity and WarehouseModel."""

    @staticmethod
    def to_entity(model: WarehouseModel) -> Warehouse:
        """Convert WarehouseModel to Warehouse entity."""

        entity = Warehouse(
            name=model.name,
            location_code=model.location_code,
            is_active=model.is_active,
        )
        entity.id = model.id
        return entity

    @staticmethod
    def to_model(entity: Warehouse) -> WarehouseModel:
        """Convert Warehouse entity to WarehouseModel."""

        return WarehouseModel(
            id=entity.id,
            name=entity.name,
            location_code=entity.location_code,
            is_active=entity.is_active,
        )

    @staticmethod
    def update_model(model: WarehouseModel, entity: Warehouse) -> WarehouseModel:
        """Update WarehouseModel fields from Warehouse entity."""

        model.name = entity.name
        model.location_code = entity.location_code
        model.is_active = entity.is_active
        return model
