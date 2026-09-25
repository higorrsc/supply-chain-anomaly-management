import asyncio
from collections import defaultdict

from src.core.domain.events import DomainEvent, EventDispatcher, EventHandler


class AsyncEventDispatcher(EventDispatcher):
    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: type[DomainEvent], handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])
        for handler in handlers:
            _task: asyncio.Task[None] = asyncio.create_task(handler(event))
            del _task
