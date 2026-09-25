from decimal import Decimal

import pytest

from src.core.domain import DomainError
from src.inventory.domain.value_objects import Quantity


class TestQuantity:
    """Test suite for quantity value object"""

    def test_if_can_create_valid_value_object(self) -> None:
        """Test if can create valid value object with valid data"""

        vo = Quantity(value=Decimal("1"))

        assert vo is not None

    def test_if_invalid_value_raises_error(self) -> None:
        """Test if invalid value raises error"""

        with pytest.raises(DomainError) as exc_info:
            Quantity(value=Decimal("-1"))

        assert "Quantity must be strictly greater than zero." in str(exc_info)
