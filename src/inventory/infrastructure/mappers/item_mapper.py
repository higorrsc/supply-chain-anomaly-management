from src.inventory.domain.entities import Item
from src.inventory.domain.value_objects import SKU
from src.inventory.infrastructure.models import ItemModel


class ItemMapper:
    """Mapper for Item entity and ItemModel."""

    @staticmethod
    def to_entity(model: ItemModel) -> Item:
        """Convert ItemModel to Item entity."""

        entity = Item(
            sku=SKU(value=model.sku),
            description=model.description,
            is_active=model.is_active,
        )
        entity.id = model.id
        # Note: created_at and updated_at exist in AbstractEntity if implemented,
        # but AbstractEntity in this project typically just holds `id`.
        # If it holds dates, we would map them here.
        return entity

    @staticmethod
    def to_model(entity: Item) -> ItemModel:
        """Convert Item entity to ItemModel."""

        return ItemModel(
            id=entity.id,
            sku=entity.sku.value,
            description=entity.description,
            is_active=entity.is_active,
        )

    @staticmethod
    def update_model(model: ItemModel, entity: Item) -> ItemModel:
        """Update ItemModel fields from Item entity."""

        model.sku = entity.sku.value
        model.description = entity.description
        model.is_active = entity.is_active
        return model
