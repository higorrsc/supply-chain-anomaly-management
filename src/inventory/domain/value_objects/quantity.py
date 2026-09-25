from dataclasses import dataclass
from decimal import Decimal

from src.core.domain import AbstractValueObject, DomainError


@dataclass(kw_only=True, frozen=True)
class Quantity(AbstractValueObject):
    """Value object that represents quantity as Decimal value"""

    value: Decimal

    def validate(self) -> None:
        """Validate the value object."""

        if self.value <= Decimal("0"):
            raise DomainError("Quantity must be strictly greater than zero.")
