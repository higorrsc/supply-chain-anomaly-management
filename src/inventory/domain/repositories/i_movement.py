from src.core.domain import AbstractRepository
from src.inventory.domain.entities import Movement


class IMovementRepository(AbstractRepository[Movement]):
    """Interface for the Movement Repository."""
