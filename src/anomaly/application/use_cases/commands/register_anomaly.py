import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.anomaly.domain.value_objects.score import Score


@dataclass(frozen=True)
class RegisterAnomalyRequestDTO:
    """Data Transfer Object for register anomaly requests."""

    movement_id: uuid.UUID
    item_id: uuid.UUID
    score: Decimal
    severity: AnomalySeverity
    detected_at: datetime


class RegisterAnomalyUseCase:
    """Use case for registering a new anomaly."""

    def __init__(self, repository: IAnomalyRepository) -> None:
        """Initialize the use case."""
        self._repository = repository

    async def execute(self, request: RegisterAnomalyRequestDTO) -> Anomaly:
        """Execute the use case."""

        anomaly = Anomaly(
            movement_id=request.movement_id,
            item_id=request.item_id,
            score=Score(value=request.score),
            severity=request.severity,
            detected_at=request.detected_at,
        )

        anomaly.validate()

        return await self._repository.save(anomaly)
