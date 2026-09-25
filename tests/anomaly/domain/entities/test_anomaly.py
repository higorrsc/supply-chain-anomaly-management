import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.exceptions import InvalidAnomalyError
from src.anomaly.domain.value_objects.score import Score


class TestAnomaly:
    """Test suite for the Anomaly entity."""

    def test_can_create_valid_anomaly(self) -> None:
        """Test creating a valid anomaly."""
        movement_id = uuid.uuid4()
        item_id = uuid.uuid4()

        anomaly = Anomaly(
            movement_id=movement_id,
            item_id=item_id,
            score=Score(value=Decimal("85.5")),
            severity=AnomalySeverity.CRITICAL,
            detected_at=datetime.now(UTC),
        )

        assert anomaly.movement_id == movement_id
        assert anomaly.item_id == item_id
        assert anomaly.score.value == Decimal("85.5")
        assert anomaly.severity == AnomalySeverity.CRITICAL
        assert anomaly.status == AnomalyStatus.OPEN

    def test_invalid_movement_id_raises_error(self) -> None:
        """Test invalid movement_id raises validation error."""
        with pytest.raises(InvalidAnomalyError) as exc_info:
            Anomaly(
                movement_id="invalid-uuid",  # type: ignore
                item_id=uuid.uuid4(),
                score=Score(value=Decimal("50.0")),
                severity=AnomalySeverity.HIGH,
                detected_at=datetime.now(UTC),
            )
        assert str(exc_info.value) == "Movement ID must be a valid UUID."

    def test_invalid_item_id_raises_error(self) -> None:
        """Test invalid item_id raises validation error."""
        with pytest.raises(InvalidAnomalyError) as exc_info:
            Anomaly(
                movement_id=uuid.uuid4(),
                item_id="invalid-uuid",  # type: ignore
                score=Score(value=Decimal("50.0")),
                severity=AnomalySeverity.HIGH,
                detected_at=datetime.now(UTC),
            )
        assert str(exc_info.value) == "Item ID must be a valid UUID."

    def test_naive_datetime_raises_error(self) -> None:
        """Test naive datetime raises validation error."""
        with pytest.raises(InvalidAnomalyError) as exc_info:
            Anomaly(
                movement_id=uuid.uuid4(),
                item_id=uuid.uuid4(),
                score=Score(value=Decimal("50.0")),
                severity=AnomalySeverity.HIGH,
                detected_at=datetime.now(),  # naive datetime
            )
        assert str(exc_info.value) == "Detected date must be timezone-aware."

    def test_resolve_anomaly(self) -> None:
        """Test resolving an open anomaly."""
        anomaly = Anomaly(
            movement_id=uuid.uuid4(),
            item_id=uuid.uuid4(),
            score=Score(value=Decimal("50.0")),
            severity=AnomalySeverity.HIGH,
            detected_at=datetime.now(UTC),
        )

        anomaly.resolve()
        assert anomaly.status == AnomalyStatus.RESOLVED

    def test_resolve_already_resolved_anomaly_raises_error(self) -> None:
        """Test resolving a resolved anomaly raises error."""
        anomaly = Anomaly(
            movement_id=uuid.uuid4(),
            item_id=uuid.uuid4(),
            score=Score(value=Decimal("50.0")),
            severity=AnomalySeverity.HIGH,
            detected_at=datetime.now(UTC),
        )

        anomaly.resolve()

        with pytest.raises(InvalidAnomalyError) as exc_info:
            anomaly.resolve()
        assert str(exc_info.value) == "Anomaly is already resolved."
