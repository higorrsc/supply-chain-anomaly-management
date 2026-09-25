import asyncio
import pytest

from src.core.domain.events import DomainEvent
from src.core.infrastructure.events.dispatcher import AsyncEventDispatcher


class DummyEvent(DomainEvent):
    pass


class OtherEvent(DomainEvent):
    pass


@pytest.mark.asyncio
async def test_async_event_dispatcher_pub_sub():
    dispatcher = AsyncEventDispatcher()

    received_events = []

    async def dummy_handler(event: DomainEvent) -> None:
        received_events.append(event)

    dispatcher.subscribe(DummyEvent, dummy_handler)

    event = DummyEvent()
    await dispatcher.publish(event)

    await asyncio.sleep(0.01)
    assert len(received_events) == 1
    assert received_events[0] == event

    # Test that it does not receive other events
    other_event = OtherEvent()
    await dispatcher.publish(other_event)
    await asyncio.sleep(0.01)
    assert len(received_events) == 1
