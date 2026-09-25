from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .events import DomainEvent


@dataclass(kw_only=True, eq=False, repr=False)
class AbstractEntity(ABC):
    """Abstract base class for entities in domain layer"""

    id: UUID = field(default_factory=uuid4)

    _domain_events: list[DomainEvent] = field(default_factory=list, init=False)

    def add_domain_event(self, event: DomainEvent) -> None:
        """Register a new domain event."""

        self._domain_events.append(event)

    def clear_domain_events(self) -> list[DomainEvent]:
        """Clear and return the registered domain events."""

        events = self._domain_events.copy()
        self._domain_events.clear()
        return events

    def list_domain_events(self) -> tuple[DomainEvent, ...]:
        """Return a read-only view of the registered domain events."""

        return tuple(self._domain_events)

    def _repr_fields(self) -> str:
        """Returns a string representation of the entity's fields"""

        return f"id={self.id}"

    def _str_fields(self) -> str:
        """Returns a string representation of the entity's fields"""

        return f"id={self.id}"

    def __eq__(self, other: object) -> bool:
        """Check if two entities are equals by IDs"""

        if not isinstance(other, AbstractEntity):
            return False

        return self.id == other.id

    def __post_init__(self) -> None:
        """Validate the entity after initialization"""

        self.validate()

    def __repr__(self) -> str:
        """Returns a detailed string representation of the class"""

        return f"<{self.__class__.__name__} {self._repr_fields()}>"

    def __str__(self) -> str:
        """Returns a string representation of the class"""

        return f"{self.__class__.__name__} ({self._repr_fields()})"

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the entity.

        This method should be implemented in the concrete subclasses to validate
        the entity's state. It should raise a ValueError if the entity is in an
        invalid state.

        Raises:
            ValueError: If the entity is in an invalid state.
        """

        raise NotImplementedError
