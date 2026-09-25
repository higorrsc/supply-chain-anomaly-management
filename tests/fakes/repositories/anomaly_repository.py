from src.core.infrastructure.repositories.in_memory_repository import InMemoryRepository
from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository

class FakeAnomalyRepository(InMemoryRepository[Anomaly], IAnomalyRepository):
    """Fake repository for Anomaly."""
