import pytest

from src.core.domain import DomainError
from src.inventory.domain.value_objects import SKU


class TestSKU:
    """Test suite for SKU value object"""

    def test_if_can_create_valid_sku(self) -> None:
        """Test if can create a valid SKU with valid data"""

        vo = SKU(value="CEL-SSG-S26U")

        assert vo is not None

    def test_if_empty_sku_value_raises_error(self) -> None:
        """Test if raises error when create SKU with empty value"""

        with pytest.raises(DomainError) as exc_info:
            SKU(value="")

        assert "The SKU must be a non-empty string." in str(exc_info)

        with pytest.raises(DomainError) as exc_info:
            SKU(value=None)  # type: ignore

        assert "The SKU must be a non-empty string." in str(exc_info)

    def test_if_short_or_long_sku_value_raises_error(self) -> None:
        """Test if raises error when create SKU to short or to long"""

        with pytest.raises(DomainError) as exc_info:
            SKU(value="SMALL")

        assert "The SKU length must be between 8 and 12 characters long." in str(
            exc_info
        )

        with pytest.raises(DomainError) as exc_info:
            SKU(value="TO-BIG-SKU-VALUE")

        assert "The SKU length must be between 8 and 12 characters long." in str(
            exc_info
        )

    def test_if_use_invalid_lower_case_and_spaces_characters_raises_error(self) -> None:
        """Test if raises error when create SKU with invalid characters"""

        with pytest.raises(DomainError) as exc_info:
            SKU(value="lower case")

        assert "The SKU cannot have lower case or spaces." in str(exc_info)
