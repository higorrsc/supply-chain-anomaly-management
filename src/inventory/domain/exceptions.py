"""Domain exceptions for Inventory bounded context."""

from src.core.domain.exceptions import EntityNotFoundError, EntityValidationError


class ItemNotFoundError(EntityNotFoundError):
    """Exception raised when an Item is not found in the repository."""


class InvalidItemError(EntityValidationError):
    """Exception raised when an Item is not valid."""


class WarehouseNotFoundError(EntityNotFoundError):
    """Exception raised when an Warehouse is not found in the repository."""


class InvalidWarehouseError(EntityValidationError):
    """Exception raised when an Warehouse is not valid."""


class InvalidMovementError(EntityValidationError):
    """Exception raised when an Movement is not valid."""
