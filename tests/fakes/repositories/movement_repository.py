from src.core.infrastructure.repositories import InMemoryRepository
from src.inventory.domain.entities import Movement
from src.inventory.domain.repositories import IMovementRepository


class FakeMovementRepository(InMemoryRepository[Movement], IMovementRepository):
    """Fake Movement Repository that satisfies IMovementRepository for testing."""
