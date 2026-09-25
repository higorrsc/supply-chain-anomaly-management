from dataclasses import dataclass
from decimal import Decimal

from src.anomaly.domain.exceptions import InvalidScoreError
from src.core.domain import AbstractValueObject


@dataclass(frozen=True, kw_only=True)
class Score(AbstractValueObject):
    """Value object representing an anomaly score."""

    value: Decimal

    def validate(self) -> None:
        """Validate the score value."""

        if self.value < Decimal("0.0"):
            raise InvalidScoreError("The anomaly score cannot be negative.")

        # Upper bound depends on the statistical model, assume max 100.0
        # Or no strict upper bound if it's z-score based. Let's just limit to positive.
        # Requirement ensures min/max validation. Limit to 100 max.
        if self.value > Decimal("100.0"):
            raise InvalidScoreError("The anomaly score cannot exceed 100.0.")
