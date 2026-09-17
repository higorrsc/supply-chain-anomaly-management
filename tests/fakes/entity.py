from dataclasses import dataclass

from src.core.domain import AbstractEntity, EntityValidationError


@dataclass(kw_only=True, eq=False, repr=False)
class FakeEntity(AbstractEntity):
    """Fake entity for tests"""

    description: str

    def validate(self) -> None:
        if not self.description or not self.description.strip():
            raise EntityValidationError("Description must be a non-empty string.")
