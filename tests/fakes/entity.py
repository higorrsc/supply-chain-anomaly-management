from dataclasses import dataclass, field

from src.core.domain import AbstractEntity, EntityValidationError


@dataclass(kw_only=True, eq=False, repr=False)
class FakeEntity(AbstractEntity):
    """Fake entity for tests"""

    description: str
    is_active: bool = field(default=True)

    def validate(self) -> None:
        if not self.description or not self.description.strip():
            raise EntityValidationError("Description must be a non-empty string.")

    def deactivate(self) -> None:
        """Inactivate the item."""

        if not self.is_active:
            raise EntityValidationError("Entity already inactive.")

        self.is_active = False

    def activate(self) -> None:
        """Activate the item."""

        if self.is_active:
            raise EntityValidationError("Entity already active.")

        self.is_active = True
