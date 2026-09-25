from src.anomaly.application.exceptions import AnomalyNotFoundError
from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.repositories.i_anomaly import IAnomalyRepository
from src.core.application.use_cases.queries.generic_get_by_id import (
    GenericGetByIdUseCase,
)


class GetAnomalyByIdUseCase(GenericGetByIdUseCase[Anomaly]):
    """Use case to get an anomaly by its id."""

    def __init__(self, repository: IAnomalyRepository) -> None:
        """Initialize the use case."""

        super().__init__(
            repository=repository,
            not_found_exception=AnomalyNotFoundError,
            not_found_message="Anomaly with ID {id} not found.",
        )
