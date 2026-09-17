from dataclasses import dataclass

from src.core.domain import AbstractEntity, EntityValidationError


@dataclass(kw_only=True, eq=False, repr=False)
class Warehouse(AbstractEntity):
    """Class representing an inventory warehouse"""

    name: str
    location_code: str
    is_active: bool

    def validate(self) -> None:
        """Validate item creation"""

        if not self.name or not self.name.strip():
            raise EntityValidationError("Name must be a non-empty string.")

        if not self.location_code or not self.location_code.strip():
            raise EntityValidationError("Location Code must be a non-empty string.")

    def deactivate(self) -> None:
        """Inactivate the warehouse."""

        if not self.is_active:
            raise EntityValidationError("Warehouse already inactive.")

        self.is_active = False

    def activate(self) -> None:
        """Activate the warehouse."""

        if self.is_active:
            raise EntityValidationError("Warehouse already active.")

        self.is_active = True
