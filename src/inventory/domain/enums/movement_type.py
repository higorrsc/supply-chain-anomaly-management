from enum import StrEnum, auto


class MovementType(StrEnum):
    """Enum representing an inventory movement type in a warehouse"""

    IN = auto()
    OUT = auto()
    ADJ = auto()
