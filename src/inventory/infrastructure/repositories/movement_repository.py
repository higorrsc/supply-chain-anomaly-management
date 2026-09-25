from src.core.infrastructure.repositories.sqlalchemy_repository import (
    SqlAlchemyRepository,
)
from src.inventory.domain.entities import Movement
from src.inventory.domain.repositories import IMovementRepository
from src.inventory.infrastructure.mappers import MovementMapper
from src.inventory.infrastructure.models import MovementModel


class MovementRepository(
    SqlAlchemyRepository[Movement, MovementModel],
    IMovementRepository,
):
    """Physical repository for Movement."""

    @property
    def model_class(self) -> type[MovementModel]:
        return MovementModel

    def _to_entity(self, model: MovementModel) -> Movement:
        return MovementMapper.to_entity(model)

    def _to_model(self, entity: Movement) -> MovementModel:
        return MovementMapper.to_model(entity)

    def _update_model(self, model: MovementModel, entity: Movement) -> MovementModel:
        return MovementMapper.update_model(model, entity)
