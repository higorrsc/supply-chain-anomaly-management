import uuid
from collections.abc import Sequence

from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.core.domain import AbstractRepository


class IAnomalyAlertRepository(AbstractRepository[AnomalyAlert]):
    """Interface for the Anomaly Alert Repository."""

    async def get_by_anomaly_id(self, anomaly_id: uuid.UUID) -> Sequence[AnomalyAlert]:
        """Get Anomaly Alerts by their associated anomaly ID."""
        raise NotImplementedError
