from enum import StrEnum, auto


class AnomalyStatus(StrEnum):
    """Enum representing the lifecycle status of an anomaly"""

    OPEN = auto()
    RESOLVED = auto()
