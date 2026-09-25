import uuid
from dataclasses import dataclass
from datetime import datetime

from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.domain.repositories.i_anomaly_alert import IAnomalyAlertRepository


@dataclass(frozen=True)
class GenerateAnomalyAlertRequestDTO:
    """Data Transfer Object for generate anomaly alert requests."""

    anomaly_id: uuid.UUID
    message: str
    generated_at: datetime


class GenerateAnomalyAlertUseCase:
    """Use case for generating a new anomaly alert."""

    def __init__(self, repository: IAnomalyAlertRepository) -> None:
        """Initialize the use case."""
        self._repository = repository

    async def execute(self, request: GenerateAnomalyAlertRequestDTO) -> AnomalyAlert:
        """Execute the use case."""

        alert = AnomalyAlert(
            anomaly_id=request.anomaly_id,
            message=request.message,
            generated_at=request.generated_at,
        )

        alert.validate()

        return await self._repository.save(alert)
