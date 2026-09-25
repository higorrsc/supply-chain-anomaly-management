from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.core.application.use_cases.queries import GenericSearchUseCase


class SearchAnomalyUseCase(GenericSearchUseCase[Anomaly]):
    """Use case to search anomalies."""

    def __init__(self, repository: IAnomalyRepository) -> None:
        """Initialize the use case."""

        super().__init__(repository=repository)
