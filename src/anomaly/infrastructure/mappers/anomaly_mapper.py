from datetime import UTC

from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.value_objects.score import Score
from src.anomaly.infrastructure.models.anomaly_model import AnomalyModel


class AnomalyMapper:
    """Mapper for Anomaly entity and AnomalyModel."""

    @staticmethod
    def to_entity(model: AnomalyModel) -> Anomaly:
        """Convert AnomalyModel to Anomaly entity."""

        entity = Anomaly(
            movement_id=model.movement_id,
            item_id=model.item_id,
            score=Score(value=model.score),
            severity=AnomalySeverity(model.severity),
            status=AnomalyStatus(model.status),
            detected_at=model.detected_at
            if model.detected_at.tzinfo
            else model.detected_at.replace(tzinfo=UTC),
        )
        entity.id = model.id
        return entity

    @staticmethod
    def to_model(entity: Anomaly) -> AnomalyModel:
        """Convert Anomaly entity to AnomalyModel."""

        return AnomalyModel(
            id=entity.id,
            movement_id=entity.movement_id,
            item_id=entity.item_id,
            score=entity.score.value,
            severity=entity.severity.value,
            status=entity.status.value,
            detected_at=entity.detected_at,
        )

    @staticmethod
    def update_model(model: AnomalyModel, entity: Anomaly) -> AnomalyModel:
        """Update AnomalyModel fields from Anomaly entity."""

        model.score = entity.score.value
        model.severity = entity.severity.value
        model.status = entity.status.value
        # movement_id, item_id, and detected_at usually do not change
        return model
