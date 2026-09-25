from dataclasses import dataclass, field
from decimal import Decimal

from src.core.domain import AbstractValueObject, DomainError


@dataclass(kw_only=True, frozen=True)
class FakeMoneyValueObject(AbstractValueObject):
    """Value object that represents a money"""

    value: Decimal
    currency: str

    _available_currencies: list[str] = field(
        default_factory=lambda: [
            "BRL",
            "USD",
            "CAD",
            "EUR",
        ]
    )

    def validate(self) -> None:
        """Validate value object creation"""

        if self.value < Decimal(0):
            raise DomainError("Value must be greater or equal to zero.")

        if not self.currency or not self.currency.strip():
            raise DomainError("Currency must be a non-empty string.")

        if self.currency not in self._available_currencies:
            raise DomainError(
                "Currency must be one of those: "
                f"{', '.join(self._available_currencies)}"
            )
