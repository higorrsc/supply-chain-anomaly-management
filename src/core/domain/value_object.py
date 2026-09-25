from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class AbstractValueObject(ABC):
    """Abstract base class for value objects"""

    def __post_init__(self) -> None:
        """Validate the entity after initialization"""

        self.validate()

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the value object.

        This method should be implemented in the concrete subclasses to validate
        the value object's state. It should raise a ValueError if the value
        object is in an invalid state.

        Raises:
            ValueError: If the value object is in an invalid state.
        """

        raise NotImplementedError
