import uuid
from datetime import UTC, datetime
from decimal import Decimal

from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.value_objects.score import Score
from src.anomaly.infrastructure.mappers.anomaly_mapper import AnomalyMapper
from src.anomaly.infrastructure.models.anomaly_model import AnomalyModel


class TestAnomalyMapper:
    """Test suite for AnomalyMapper."""

    def test_to_entity(self) -> None:
        """Test conversion from model to entity."""

        model = AnomalyModel(
            id=uuid.uuid4(),
            movement_id=uuid.uuid4(),
            item_id=uuid.uuid4(),
            score=Decimal("95.00"),
            severity="critical",
            status="open",
            detected_at=datetime.now(UTC),
        )

        entity = AnomalyMapper.to_entity(model)

        assert entity.id == model.id
        assert entity.movement_id == model.movement_id
        assert entity.item_id == model.item_id
        assert entity.score.value == model.score
        assert entity.severity.value == model.severity
        assert entity.status.value == model.status
        assert entity.detected_at == model.detected_at

    def test_to_model(self) -> None:
        """Test conversion from entity to model."""

        entity = Anomaly(
            movement_id=uuid.uuid4(),
            item_id=uuid.uuid4(),
            score=Score(value=Decimal("80.50")),
            severity=AnomalySeverity.HIGH,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )

        model = AnomalyMapper.to_model(entity)

        assert model.id == entity.id
        assert model.movement_id == entity.movement_id
        assert model.item_id == entity.item_id
        assert model.score == entity.score.value
        assert model.severity == entity.severity.value
        assert model.status == entity.status.value
        assert model.detected_at == entity.detected_at

    def test_update_model(self) -> None:
        """Test updating model from entity."""

        model = AnomalyModel(
            id=uuid.uuid4(),
            movement_id=uuid.uuid4(),
            item_id=uuid.uuid4(),
            score=Decimal("80.50"),
            severity="high",
            status="open",
            detected_at=datetime.now(UTC),
        )

        entity = Anomaly(
            movement_id=model.movement_id,
            item_id=model.item_id,
            score=Score(value=Decimal("80.50")),
            severity=AnomalySeverity.HIGH,
            status=AnomalyStatus.RESOLVED,
            detected_at=model.detected_at,
        )

        updated_model = AnomalyMapper.update_model(model, entity)

        assert updated_model.score == Decimal("80.50")
        assert updated_model.severity == "high"
        assert updated_model.status == "resolved"
