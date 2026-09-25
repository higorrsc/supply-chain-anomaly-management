import uuid
from collections.abc import Sequence

from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.domain.repositories.i_anomaly_alert import IAnomalyAlertRepository


class GetAlertsByAnomalyIdUseCase:
    """Use case to get anomaly alerts by anomaly id."""

    def __init__(self, repository: IAnomalyAlertRepository) -> None:
        """Initialize the use case."""
        self._repository = repository

    async def execute(self, anomaly_id: uuid.UUID) -> Sequence[AnomalyAlert]:
        """Execute the use case."""
        return await self._repository.get_by_anomaly_id(anomaly_id)
