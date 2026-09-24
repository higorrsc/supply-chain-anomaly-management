from sqlalchemy import select

from src.core.infrastructure.repositories.sqlalchemy_repository import (
    SqlAlchemyRepository,
)
from src.inventory.domain.entities import Item
from src.inventory.domain.repositories import IItemRepository
from src.inventory.domain.value_objects import SKU
from src.inventory.infrastructure.mappers import ItemMapper
from src.inventory.infrastructure.models import ItemModel


class ItemRepository(
    SqlAlchemyRepository[Item, ItemModel],
    IItemRepository,
):
    """Physical repository for Item."""

    @property
    def model_class(self) -> type[ItemModel]:
        return ItemModel

    def _to_entity(self, model: ItemModel) -> Item:
        return ItemMapper.to_entity(model)

    def _to_model(self, entity: Item) -> ItemModel:
        return ItemMapper.to_model(entity)

    def _update_model(self, model: ItemModel, entity: Item) -> ItemModel:
        return ItemMapper.update_model(model, entity)

    async def get_by_sku(self, sku: SKU) -> Item | None:
        """Retrieve an item by its SKU."""

        stmt = select(self.model_class).where(self.model_class.sku == sku.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_entity(model)
