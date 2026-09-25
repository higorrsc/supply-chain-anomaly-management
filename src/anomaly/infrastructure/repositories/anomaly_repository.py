from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.anomaly.infrastructure.mappers.anomaly_mapper import AnomalyMapper
from src.anomaly.infrastructure.models.anomaly_model import AnomalyModel
from src.core.infrastructure.repositories.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class AnomalyRepository(
    SqlAlchemyRepository[Anomaly, AnomalyModel],
    IAnomalyRepository,
):
    """Physical repository for Anomaly."""

    @property
    def model_class(self) -> type[AnomalyModel]:
        return AnomalyModel

    def _to_entity(self, model: AnomalyModel) -> Anomaly:
        return AnomalyMapper.to_entity(model)

    def _to_model(self, entity: Anomaly) -> AnomalyModel:
        return AnomalyMapper.to_model(entity)

    def _update_model(self, model: AnomalyModel, entity: Anomaly) -> AnomalyModel:
        return AnomalyMapper.update_model(model, entity)
