import uuid
from dataclasses import dataclass
from datetime import datetime

from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.exceptions import InvalidAnomalyError
from src.anomaly.domain.value_objects.score import Score
from src.core.domain import AbstractEntity


@dataclass(kw_only=True, eq=False, repr=False)
class Anomaly(AbstractEntity):
    """Class representing an anomaly detected in the supply chain."""

    movement_id: uuid.UUID
    item_id: uuid.UUID
    score: Score
    severity: AnomalySeverity
    status: AnomalyStatus = AnomalyStatus.OPEN
    detected_at: datetime

    def validate(self) -> None:
        """Validate anomaly creation."""

        if not isinstance(self.movement_id, uuid.UUID):
            raise InvalidAnomalyError("Movement ID must be a valid UUID.")

        if not isinstance(self.item_id, uuid.UUID):
            raise InvalidAnomalyError("Item ID must be a valid UUID.")

        if self.detected_at.tzinfo is None:
            raise InvalidAnomalyError("Detected date must be timezone-aware.")

    def resolve(self) -> None:
        """Resolve the anomaly."""

        if self.status == AnomalyStatus.RESOLVED:
            raise InvalidAnomalyError("Anomaly is already resolved.")

        self.status = AnomalyStatus.RESOLVED
