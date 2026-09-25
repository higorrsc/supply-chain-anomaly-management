import uuid
from datetime import UTC, datetime

from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.infrastructure.mappers.anomaly_alert_mapper import AnomalyAlertMapper
from src.anomaly.infrastructure.models.anomaly_alert_model import AnomalyAlertModel


class TestAnomalyAlertMapper:
    """Test suite for AnomalyAlertMapper."""

    def test_to_entity(self) -> None:
        """Test conversion from model to entity."""

        model = AnomalyAlertModel(
            id=uuid.uuid4(),
            anomaly_id=uuid.uuid4(),
            message="Test alert",
            is_read=True,
            generated_at=datetime.now(UTC),
        )

        entity = AnomalyAlertMapper.to_entity(model)

        assert entity.id == model.id
        assert entity.anomaly_id == model.anomaly_id
        assert entity.message == model.message
        assert entity.is_read == model.is_read
        assert entity.generated_at == model.generated_at

    def test_to_model(self) -> None:
        """Test conversion from entity to model."""

        entity = AnomalyAlert(
            anomaly_id=uuid.uuid4(),
            message="Another test alert",
            is_read=False,
            generated_at=datetime.now(UTC),
        )

        model = AnomalyAlertMapper.to_model(entity)

        assert model.id == entity.id
        assert model.anomaly_id == entity.anomaly_id
        assert model.message == entity.message
        assert model.is_read == entity.is_read
        assert model.generated_at == entity.generated_at

    def test_update_model(self) -> None:
        """Test updating model from entity."""

        model = AnomalyAlertModel(
            id=uuid.uuid4(),
            anomaly_id=uuid.uuid4(),
            message="Old message",
            is_read=False,
            generated_at=datetime.now(UTC),
        )

        entity = AnomalyAlert(
            anomaly_id=model.anomaly_id,
            message="New message",
            is_read=True,
            generated_at=model.generated_at,
        )

        updated_model = AnomalyAlertMapper.update_model(model, entity)

        assert updated_model.message == "New message"
        assert updated_model.is_read is True
