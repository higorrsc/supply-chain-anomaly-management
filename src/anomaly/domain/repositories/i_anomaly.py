import uuid

from src.anomaly.domain.entities.anomaly import Anomaly
from src.core.domain import AbstractRepository


class IAnomalyRepository(AbstractRepository[Anomaly]):
    """Interface for the Anomaly Repository."""

    async def get_by_movement_id(self, movement_id: uuid.UUID) -> Anomaly | None:
        """Get an Anomaly by its associated movement ID."""
        raise NotImplementedError
