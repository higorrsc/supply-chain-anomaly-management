from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.anomaly.domain.repositories.i_anomaly_alert import IAnomalyAlertRepository
from src.core.domain import AbstractRepository


class TestAnomalyRepositoriesInterfaces:
    """Test suite for anomaly repository interfaces."""

    def test_i_anomaly_repository_inherits_abstract_repository(self) -> None:
        """Verify IAnomalyRepository inherits from AbstractRepository."""
        assert issubclass(IAnomalyRepository, AbstractRepository)

    def test_i_anomaly_alert_repository_inherits_abstract_repository(self) -> None:
        """Verify IAnomalyAlertRepository inherits from AbstractRepository."""
        assert issubclass(IAnomalyAlertRepository, AbstractRepository)
