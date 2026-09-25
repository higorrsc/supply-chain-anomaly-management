import uuid
from datetime import UTC, datetime

import pytest

from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.domain.exceptions import InvalidAnomalyError


class TestAnomalyAlert:
    """Test suite for the AnomalyAlert entity."""

    def test_can_create_valid_alert(self) -> None:
        """Test creating a valid anomaly alert."""
        anomaly_id = uuid.uuid4()
        alert = AnomalyAlert(
            anomaly_id=anomaly_id,
            message="Critical anomaly detected in stock.",
            generated_at=datetime.now(UTC),
        )

        assert alert.anomaly_id == anomaly_id
        assert alert.message == "Critical anomaly detected in stock."
        assert alert.is_read is False

    def test_invalid_anomaly_id_raises_error(self) -> None:
        """Test invalid anomaly_id raises validation error."""
        with pytest.raises(InvalidAnomalyError) as exc_info:
            AnomalyAlert(
                anomaly_id="invalid-uuid",  # type: ignore
                message="Critical anomaly detected.",
                generated_at=datetime.now(UTC),
            )
        assert str(exc_info.value) == "Anomaly ID must be a valid UUID."

    def test_empty_message_raises_error(self) -> None:
        """Test empty message raises validation error."""
        with pytest.raises(InvalidAnomalyError) as exc_info:
            AnomalyAlert(
                anomaly_id=uuid.uuid4(),
                message="   ",
                generated_at=datetime.now(UTC),
            )
        assert str(exc_info.value) == "Alert message cannot be empty."

    def test_naive_datetime_raises_error(self) -> None:
        """Test naive datetime raises validation error."""
        with pytest.raises(InvalidAnomalyError) as exc_info:
            AnomalyAlert(
                anomaly_id=uuid.uuid4(),
                message="Critical anomaly detected.",
                generated_at=datetime.now(),  # naive datetime
            )
        assert str(exc_info.value) == "Generation date must be timezone-aware."

    def test_mark_as_read(self) -> None:
        """Test marking an alert as read."""
        alert = AnomalyAlert(
            anomaly_id=uuid.uuid4(),
            message="Critical anomaly detected.",
            generated_at=datetime.now(UTC),
        )

        alert.mark_as_read()
        assert alert.is_read is True

    def test_mark_already_read_alert_raises_error(self) -> None:
        """Test marking a read alert raises validation error."""
        alert = AnomalyAlert(
            anomaly_id=uuid.uuid4(),
            message="Critical anomaly detected.",
            generated_at=datetime.now(UTC),
        )

        alert.mark_as_read()

        with pytest.raises(InvalidAnomalyError) as exc_info:
            alert.mark_as_read()
        assert str(exc_info.value) == "Alert is already marked as read."
