from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol
from uuid import UUID, uuid4


@dataclass(kw_only=True, frozen=True)
class DomainEvent:
    """Abstract base class for domain events"""

    event_id: UUID = field(default_factory=uuid4)
    occurred_on: datetime = field(default_factory=lambda: datetime.now(UTC))


EventHandler = Callable[[DomainEvent], Awaitable[None]]


class EventDispatcher(Protocol):
    def subscribe(self, event_type: type[DomainEvent], handler: EventHandler) -> None:
        """Subscribes a handler to a specific event type."""

    async def publish(self, event: DomainEvent) -> None:
        """Publishes an event to all registered handlers."""
