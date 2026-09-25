import uuid
from dataclasses import dataclass

from src.anomaly.application.exceptions import AnomalyNotFoundError
from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository


@dataclass(frozen=True)
class ResolveAnomalyRequestDTO:
    """Data Transfer Object for resolve anomaly requests."""

    anomaly_id: uuid.UUID


class ResolveAnomalyUseCase:
    """Use case for resolving an anomaly."""

    def __init__(self, repository: IAnomalyRepository) -> None:
        """Initialize the use case."""
        self._repository = repository

    async def execute(self, request: ResolveAnomalyRequestDTO) -> Anomaly:
        """Execute the use case."""

        anomaly = await self._repository.get_by_id(request.anomaly_id)
        if not anomaly:
            raise AnomalyNotFoundError(f"Anomaly {request.anomaly_id} not found.")

        anomaly.resolve()

        return await self._repository.save(anomaly)
