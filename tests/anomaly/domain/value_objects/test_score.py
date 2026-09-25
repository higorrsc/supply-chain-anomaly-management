from decimal import Decimal

import pytest

from src.anomaly.domain.exceptions import InvalidScoreError
from src.anomaly.domain.value_objects.score import Score


class TestScore:
    """Test suite for the Score value object."""

    def test_can_create_valid_score(self) -> None:
        """Test creating a valid score."""
        score = Score(value=Decimal("50.5"))
        assert score.value == Decimal("50.5")

    def test_negative_score_raises_error(self) -> None:
        """Test negative score raises validation error."""
        with pytest.raises(InvalidScoreError) as exc_info:
            Score(value=Decimal("-1.0"))

        assert str(exc_info.value) == "The anomaly score cannot be negative."

    def test_score_above_max_raises_error(self) -> None:
        """Test score above maximum raises validation error."""
        with pytest.raises(InvalidScoreError) as exc_info:
            Score(value=Decimal("100.1"))

        assert str(exc_info.value) == "The anomaly score cannot exceed 100.0."
