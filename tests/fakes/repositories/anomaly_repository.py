from src.anomaly.domain.entities import Anomaly
from src.anomaly.domain.repositories import IAnomalyRepository
from src.core.infrastructure.repositories import InMemoryRepository


class FakeAnomalyRepository(InMemoryRepository[Anomaly], IAnomalyRepository):
    """Fake repository for Anomaly."""
