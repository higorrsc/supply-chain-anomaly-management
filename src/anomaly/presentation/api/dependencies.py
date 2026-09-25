from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.anomaly.application.use_cases.commands.register_anomaly import (
    RegisterAnomalyUseCase,
)
from src.anomaly.application.use_cases.commands.resolve_anomaly import (
    ResolveAnomalyUseCase,
)
from src.anomaly.application.use_cases.queries.get_alerts_by_anomaly_id import (
    GetAlertsByAnomalyIdUseCase,
)
from src.anomaly.application.use_cases.queries.get_anomaly_by_id import (
    GetAnomalyByIdUseCase,
)
from src.anomaly.application.use_cases.queries.search_anomaly import (
    SearchAnomalyUseCase,
)
from src.anomaly.infrastructure.repositories.anomaly_alert_repository import (
    AnomalyAlertRepository,
)
from src.anomaly.infrastructure.repositories.anomaly_repository import AnomalyRepository
from src.core.infrastructure.database.session import get_db_session

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_anomaly_repository(session: SessionDep) -> AnomalyRepository:
    return AnomalyRepository(session=session)


def get_anomaly_alert_repository(session: SessionDep) -> AnomalyAlertRepository:
    return AnomalyAlertRepository(session=session)


AnomalyRepoDep = Annotated[AnomalyRepository, Depends(get_anomaly_repository)]
AnomalyAlertRepoDep = Annotated[
    AnomalyAlertRepository, Depends(get_anomaly_alert_repository)
]


def get_register_anomaly_use_case(repo: AnomalyRepoDep) -> RegisterAnomalyUseCase:
    return RegisterAnomalyUseCase(repository=repo)


def get_resolve_anomaly_use_case(repo: AnomalyRepoDep) -> ResolveAnomalyUseCase:
    return ResolveAnomalyUseCase(repository=repo)


def get_anomaly_by_id_use_case(repo: AnomalyRepoDep) -> GetAnomalyByIdUseCase:
    return GetAnomalyByIdUseCase(repository=repo)


def get_search_anomaly_use_case(repo: AnomalyRepoDep) -> SearchAnomalyUseCase:
    return SearchAnomalyUseCase(repository=repo)


def get_alerts_by_anomaly_id_use_case(
    repo: AnomalyAlertRepoDep,
) -> GetAlertsByAnomalyIdUseCase:
    return GetAlertsByAnomalyIdUseCase(repository=repo)
