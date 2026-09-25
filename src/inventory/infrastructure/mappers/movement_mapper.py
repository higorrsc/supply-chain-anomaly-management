from src.inventory.domain.entities import Movement
from src.inventory.domain.enums import MovementType
from src.inventory.domain.value_objects import Quantity
from src.inventory.infrastructure.models import MovementModel


class MovementMapper:
    """Mapper for Movement entity and MovementModel."""

    @staticmethod
    def to_entity(model: MovementModel) -> Movement:
        """Convert MovementModel to Movement entity."""

        from datetime import UTC

        occurred_at = model.occurred_at
        if occurred_at.tzinfo is None:
            occurred_at = occurred_at.replace(tzinfo=UTC)

        entity = Movement(
            id=model.id,
            item_id=model.item_id,
            warehouse_id=model.warehouse_id,
            quantity=Quantity(value=model.quantity),
            movement_type=MovementType(model.movement_type),
            occurred_at=occurred_at,
        )
        entity.clear_domain_events()
        return entity

    @staticmethod
    def to_model(entity: Movement) -> MovementModel:
        """Convert Movement entity to MovementModel."""

        return MovementModel(
            id=entity.id,
            item_id=entity.item_id,
            warehouse_id=entity.warehouse_id,
            quantity=entity.quantity.value,
            movement_type=entity.movement_type,
            occurred_at=entity.occurred_at,
        )

    @staticmethod
    def update_model(model: MovementModel, entity: Movement) -> MovementModel:
        """Update MovementModel fields from Movement entity."""

        model.item_id = entity.item_id
        model.warehouse_id = entity.warehouse_id
        model.quantity = entity.quantity.value
        model.movement_type = entity.movement_type
        model.occurred_at = entity.occurred_at
        return model
