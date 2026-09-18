from typing import Protocol


class ActivatableEntity(Protocol):
    """Protocol defining the contract for entities that can be activated/deactivated."""

    def activate(self) -> None:
        """Action to activate an entity"""

    def deactivate(self) -> None:
        """Action to deactivate an entity"""
