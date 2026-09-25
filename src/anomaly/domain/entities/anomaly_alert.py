import uuid
from dataclasses import dataclass
from datetime import datetime

from src.anomaly.domain.exceptions import InvalidAnomalyError
from src.core.domain import AbstractEntity


@dataclass(kw_only=True, eq=False, repr=False)
class AnomalyAlert(AbstractEntity):
    """Class representing an alert generated for an anomaly."""

    anomaly_id: uuid.UUID
    message: str
    generated_at: datetime
    is_read: bool = False

    def validate(self) -> None:
        """Validate alert creation."""

        if not isinstance(self.anomaly_id, uuid.UUID):
            raise InvalidAnomalyError("Anomaly ID must be a valid UUID.")

        if not self.message or not self.message.strip():
            raise InvalidAnomalyError("Alert message cannot be empty.")

        if self.generated_at.tzinfo is None:
            raise InvalidAnomalyError("Generation date must be timezone-aware.")

    def mark_as_read(self) -> None:
        """Mark the alert as read."""

        if self.is_read:
            raise InvalidAnomalyError("Alert is already marked as read.")

        self.is_read = True
