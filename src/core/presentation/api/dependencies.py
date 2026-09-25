from src.core.infrastructure.events.dispatcher import AsyncEventDispatcher

global_event_dispatcher = AsyncEventDispatcher()


def get_event_dispatcher() -> AsyncEventDispatcher:
    return global_event_dispatcher
