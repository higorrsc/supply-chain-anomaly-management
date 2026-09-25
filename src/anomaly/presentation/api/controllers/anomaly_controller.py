from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.anomaly.application.use_cases.commands.register_anomaly import (
    RegisterAnomalyRequestDTO,
    RegisterAnomalyUseCase,
)
from src.anomaly.application.use_cases.commands.resolve_anomaly import (
    ResolveAnomalyRequestDTO,
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
from src.anomaly.presentation.api.dependencies import (
    get_alerts_by_anomaly_id_use_case,
    get_anomaly_by_id_use_case,
    get_register_anomaly_use_case,
    get_resolve_anomaly_use_case,
    get_search_anomaly_use_case,
)
from src.anomaly.presentation.api.schemas.anomaly_schema import (
    AnomalyAlertResponse,
    AnomalyResponse,
    RegisterAnomalyRequest,
    SearchAnomaliesResponse,
)
from src.core.application.use_cases.queries.generic_get_by_id import GetByIdRequestDTO
from src.core.application.use_cases.queries.generic_search import SearchRequestDTO

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])


@router.post(
    "",
    response_model=AnomalyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new anomaly",
)
async def register_anomaly(
    request: RegisterAnomalyRequest,
    use_case: Annotated[RegisterAnomalyUseCase, Depends(get_register_anomaly_use_case)],
) -> AnomalyResponse:
    """Register a new anomaly based on an event."""

    dto = RegisterAnomalyRequestDTO(
        movement_id=request.movement_id,
        item_id=request.item_id,
        score=request.score,
        severity=request.severity,
        detected_at=request.detected_at,
    )

    anomaly = await use_case.execute(dto)
    return AnomalyResponse.model_validate(anomaly)


@router.get(
    "/{anomaly_id}",
    response_model=AnomalyResponse,
    summary="Get anomaly by ID",
)
async def get_anomaly_by_id(
    anomaly_id: UUID,
    use_case: Annotated[GetAnomalyByIdUseCase, Depends(get_anomaly_by_id_use_case)],
) -> AnomalyResponse:
    """Retrieve a specific anomaly by its ID."""

    anomaly = await use_case.execute(GetByIdRequestDTO(id=anomaly_id))
    return AnomalyResponse.model_validate(anomaly)


@router.put(
    "/{anomaly_id}/resolve",
    response_model=AnomalyResponse,
    summary="Resolve an anomaly",
)
async def resolve_anomaly(
    anomaly_id: UUID,
    use_case: Annotated[ResolveAnomalyUseCase, Depends(get_resolve_anomaly_use_case)],
) -> AnomalyResponse:
    """Mark an anomaly as resolved."""

    anomaly = await use_case.execute(ResolveAnomalyRequestDTO(anomaly_id=anomaly_id))
    return AnomalyResponse.model_validate(anomaly)


@router.get(
    "/{anomaly_id}/alerts",
    response_model=list[AnomalyAlertResponse],
    summary="Get alerts for an anomaly",
)
async def get_alerts_by_anomaly_id(
    anomaly_id: UUID,
    use_case: Annotated[
        GetAlertsByAnomalyIdUseCase, Depends(get_alerts_by_anomaly_id_use_case)
    ],
) -> list[AnomalyAlertResponse]:
    """Retrieve all alerts associated with a specific anomaly."""

    alerts = await use_case.execute(anomaly_id)
    return [AnomalyAlertResponse.model_validate(alert) for alert in alerts]


@router.get(
    "",
    response_model=SearchAnomaliesResponse,
    summary="Search anomalies",
)
async def search_anomalies(
    use_case: Annotated[SearchAnomalyUseCase, Depends(get_search_anomaly_use_case)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
    status: Annotated[str | None, Query(description="Filter by status")] = None,
    severity: Annotated[str | None, Query(description="Filter by severity")] = None,
    item_id: Annotated[UUID | None, Query(description="Filter by item ID")] = None,
    movement_id: Annotated[
        UUID | None, Query(description="Filter by movement ID")
    ] = None,
) -> SearchAnomaliesResponse:
    """Search and paginate anomalies based on optional filters."""

    filters: dict[str, Any] = {}
    if status is not None:
        filters["status"] = status
    if severity is not None:
        filters["severity"] = severity
    if item_id is not None:
        filters["item_id"] = item_id
    if movement_id is not None:
        filters["movement_id"] = movement_id

    request = SearchRequestDTO(filters=filters, page=page, page_size=page_size)

    result = await use_case.execute(request)

    items = [AnomalyResponse.model_validate(item) for item in result.data]

    return SearchAnomaliesResponse(data=items, meta=result.meta)
