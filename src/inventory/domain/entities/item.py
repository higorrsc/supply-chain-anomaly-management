from dataclasses import dataclass

from src.core.domain import AbstractEntity, EntityValidationError
from src.inventory.domain.value_objects import SKU


@dataclass(kw_only=True, eq=False, repr=False)
class Item(AbstractEntity):
    """Class representing an inventory item"""

    sku: SKU
    description: str
    is_active: bool

    def validate(self) -> None:
        """Validate item creation"""

        if not self.description or not self.description.strip():
            raise EntityValidationError("Description must be a non-empty string.")

    def deactivate(self) -> None:
        """Inactivate the item."""

        if not self.is_active:
            raise EntityValidationError("Item already inactive.")

        self.is_active = False

    def activate(self) -> None:
        """Activate the item."""

        if self.is_active:
            raise EntityValidationError("Item already active.")

        self.is_active = True
