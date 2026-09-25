import uuid

from sqlalchemy import select

from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.domain.repositories.i_anomaly_alert import IAnomalyAlertRepository
from src.anomaly.infrastructure.mappers.anomaly_alert_mapper import AnomalyAlertMapper
from src.anomaly.infrastructure.models.anomaly_alert_model import AnomalyAlertModel
from src.core.infrastructure.repositories.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class AnomalyAlertRepository(
    SqlAlchemyRepository[AnomalyAlert, AnomalyAlertModel],
    IAnomalyAlertRepository,
):
    """Physical repository for AnomalyAlert."""

    @property
    def model_class(self) -> type[AnomalyAlertModel]:
        return AnomalyAlertModel

    def _to_entity(self, model: AnomalyAlertModel) -> AnomalyAlert:
        return AnomalyAlertMapper.to_entity(model)

    def _to_model(self, entity: AnomalyAlert) -> AnomalyAlertModel:
        return AnomalyAlertMapper.to_model(entity)

    def _update_model(
        self, model: AnomalyAlertModel, entity: AnomalyAlert
    ) -> AnomalyAlertModel:
        return AnomalyAlertMapper.update_model(model, entity)

    async def get_by_anomaly_id(self, anomaly_id: uuid.UUID) -> list[AnomalyAlert]:
        """Retrieve all alerts for a given anomaly ID."""

        stmt = select(self.model_class).where(self.model_class.anomaly_id == anomaly_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
