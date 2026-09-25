from src.core.domain.exceptions import DomainError


class InvalidAnomalyError(DomainError):
    """Raised when an anomaly operation or creation is invalid"""


class InvalidScoreError(DomainError):
    """Raised when an anomaly score is invalid"""
