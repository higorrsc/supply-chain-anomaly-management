from dataclasses import dataclass

from src.core.domain import DomainEvent


@dataclass(kw_only=True, frozen=True)
class FakeEvent(DomainEvent):
    """Fake domain event for tests."""

    payload: str  # type: ignore
