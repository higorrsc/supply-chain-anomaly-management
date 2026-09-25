from src.core.domain.exceptions import EntityNotFoundError

class AnomalyNotFoundError(EntityNotFoundError):
    """Raised when an anomaly is not found."""

class AnomalyAlertNotFoundError(EntityNotFoundError):
    """Raised when an anomaly alert is not found."""
