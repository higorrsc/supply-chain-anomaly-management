import pytest

from src.anomaly.application.exceptions import (
    AnomalyAlertNotFoundError,
    AnomalyNotFoundError,
)


class TestAnomalyApplicationExceptions:
    """Test suite for anomaly application exceptions."""

    def test_anomaly_not_found_error(self) -> None:
        """Test AnomalyNotFoundError can be raised."""
        with pytest.raises(AnomalyNotFoundError) as exc_info:
            raise AnomalyNotFoundError("Anomaly not found.")
        assert str(exc_info.value) == "Anomaly not found."

    def test_anomaly_alert_not_found_error(self) -> None:
        """Test AnomalyAlertNotFoundError can be raised."""
        with pytest.raises(AnomalyAlertNotFoundError) as exc_info:
            raise AnomalyAlertNotFoundError("Alert not found.")
        assert str(exc_info.value) == "Alert not found."
