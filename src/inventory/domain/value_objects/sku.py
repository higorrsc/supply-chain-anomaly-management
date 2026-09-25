import re
from dataclasses import dataclass
from typing import ClassVar

from src.core.domain import AbstractValueObject, DomainError


@dataclass(kw_only=True, frozen=True)
class SKU(AbstractValueObject):
    """
    Value object that represents unique alphanumeric code that businesses
    use internally to identify and track every distinct product and variant
    in their inventory
    """

    value: str

    _min_length: ClassVar[int] = 8
    _max_length: ClassVar[int] = 12

    def validate(self) -> None:
        """Validate the value object."""

        if not self.value or not self.value.strip():
            raise DomainError("The SKU must be a non-empty string.")

        if not self._min_length <= len(self.value) <= self._max_length:
            raise DomainError(
                f"The SKU length must be between {self._min_length} "
                f"and {self._max_length} characters long."
            )

        if re.search(r"[a-z\s]", self.value):
            raise DomainError("The SKU cannot have lower case or spaces.")
