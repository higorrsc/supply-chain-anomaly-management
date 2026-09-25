from datetime import UTC

from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.infrastructure.models.anomaly_alert_model import AnomalyAlertModel


class AnomalyAlertMapper:
    """Mapper for AnomalyAlert entity and AnomalyAlertModel."""

    @staticmethod
    def to_entity(model: AnomalyAlertModel) -> AnomalyAlert:
        """Convert AnomalyAlertModel to AnomalyAlert entity."""

        entity = AnomalyAlert(
            anomaly_id=model.anomaly_id,
            message=model.message,
            is_read=model.is_read,
            generated_at=model.generated_at
            if model.generated_at.tzinfo
            else model.generated_at.replace(tzinfo=UTC),
        )
        entity.id = model.id
        return entity

    @staticmethod
    def to_model(entity: AnomalyAlert) -> AnomalyAlertModel:
        """Convert AnomalyAlert entity to AnomalyAlertModel."""

        return AnomalyAlertModel(
            id=entity.id,
            anomaly_id=entity.anomaly_id,
            message=entity.message,
            is_read=entity.is_read,
            generated_at=entity.generated_at,
        )

    @staticmethod
    def update_model(
        model: AnomalyAlertModel, entity: AnomalyAlert
    ) -> AnomalyAlertModel:
        """Update AnomalyAlertModel fields from AnomalyAlert entity."""

        model.message = entity.message
        model.is_read = entity.is_read
        return model
