from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus


class TestAnomalyEnums:
    """Test suite for anomaly enums."""

    def test_anomaly_status_values(self) -> None:
        """Test AnomalyStatus holds expected values."""

        assert AnomalyStatus.OPEN.value == "open"
        assert AnomalyStatus.RESOLVED.value == "resolved"

    def test_anomaly_severity_values(self) -> None:
        """Test AnomalySeverity holds expected values."""

        assert AnomalySeverity.LOW.value == "low"
        assert AnomalySeverity.MEDIUM.value == "medium"
        assert AnomalySeverity.HIGH.value == "high"
        assert AnomalySeverity.CRITICAL.value == "critical"
