from enum import StrEnum, auto


class AnomalySeverity(StrEnum):
    """Enum representing the severity of an anomaly"""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()
