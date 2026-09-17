from decimal import Decimal

import pytest
from faker import Faker

from src.core.domain.exceptions import DomainError
from tests.fakes import FakeMoneyValueObject


class TestValueObject:
    """Test suite for value object"""

    def test_create_value_object_successfully(self) -> None:
        """Test if can create a value object with all data"""

        fake = Faker()
        fake_value = Decimal(fake.random_number())
        fake_currency = "BRL"

        fake_vo = FakeMoneyValueObject(value=fake_value, currency=fake_currency)

        assert fake_vo.value == fake_value
        assert fake_vo.currency == fake_currency

    def test_create_value_object_with_invalid_value_raises_error(self) -> None:
        """Test if raises error when create a value object with invalid value"""

        fake_value = Decimal(-1)
        fake_currency = "BRL"

        with pytest.raises(DomainError) as exc_info:
            FakeMoneyValueObject(value=fake_value, currency=fake_currency)

        assert "Value must be greater or equal to zero." in str(exc_info)

    def test_create_value_object_with_invalid_currency_raises_error(self) -> None:
        """Test if raises error when create a value object with invalid currency"""

        fake = Faker()
        fake_value = Decimal(fake.random_number())
        fake_currency = "GBP"

        with pytest.raises(DomainError) as exc_info:
            FakeMoneyValueObject(value=fake_value, currency=fake_currency)

        assert "Currency must be one of those:" in str(exc_info)

    def test_create_value_object_with_empty_currency_raises_error(self) -> None:
        """Test if raises error when create a value object with empty currency"""

        fake = Faker()
        fake_value = Decimal(fake.random_number())
        fake_currency = ""

        with pytest.raises(DomainError) as exc_info:
            FakeMoneyValueObject(value=fake_value, currency=fake_currency)

        assert "Currency must be a non-empty string." in str(exc_info)
