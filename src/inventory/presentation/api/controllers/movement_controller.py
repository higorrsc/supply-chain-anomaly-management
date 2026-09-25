from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.core.application.use_cases.queries import GetByIdRequestDTO, SearchRequestDTO
from src.core.domain import ConflictError
from src.inventory.application.use_cases.commands import (
    CreateMovementRequestDTO,
    CreateMovementUseCase,
)
from src.inventory.application.use_cases.queries import (
    GetMovementByIdUseCase,
    SearchMovementUseCase,
)
from src.inventory.domain.enums import MovementType
from src.inventory.domain.exceptions import (
    InvalidMovementError,
    ItemNotFoundError,
    MovementNotFoundError,
    WarehouseNotFoundError,
)
from src.inventory.presentation.api import (
    get_create_movement_use_case,
    get_movement_by_id_use_case,
    get_search_movement_use_case,
)
from src.inventory.presentation.api.schemas import (
    MovementResponse,
    RegisterMovementRequest,
    SearchMovementsResponse,
)

router = APIRouter(prefix="/movements", tags=["Movements"])


@router.post("", response_model=MovementResponse, status_code=status.HTTP_201_CREATED)
async def create_movement(
    request: RegisterMovementRequest,
    use_case: Annotated[CreateMovementUseCase, Depends(get_create_movement_use_case)],
) -> Any:
    """Create a new movement."""
    try:
        dto = CreateMovementRequestDTO(
            item_id=request.item_id,
            warehouse_id=request.warehouse_id,
            quantity=request.quantity,
            movement_type=request.movement_type.value,
            occurred_at=request.occurred_at,
        )
        movement = await use_case.execute(dto)
        return MovementResponse.model_validate(movement)
    except (ItemNotFoundError, WarehouseNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except InvalidMovementError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.get("", response_model=SearchMovementsResponse)
async def search_movements(
    use_case: Annotated[SearchMovementUseCase, Depends(get_search_movement_use_case)],
    item_id: Annotated[UUID | None, Query(description="Filter by item ID")] = None,
    warehouse_id: Annotated[
        UUID | None,
        Query(description="Filter by warehouse ID"),
    ] = None,
    movement_type: Annotated[
        MovementType | None,
        Query(description="Filter by type"),
    ] = None,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
) -> Any:
    """Search movements with pagination and filters."""
    filters: dict[str, Any] = {}
    if item_id is not None:
        filters["item_id"] = item_id
    if warehouse_id is not None:
        filters["warehouse_id"] = warehouse_id
    if movement_type is not None:
        filters["movement_type"] = movement_type

    request_dto = SearchRequestDTO(filters=filters, page=page, page_size=page_size)
    response_dto = await use_case.execute(request_dto)
    items = [MovementResponse.model_validate(item) for item in response_dto.data]
    return SearchMovementsResponse(data=items, meta=response_dto.meta)


@router.get("/{movement_id}", response_model=MovementResponse)
async def get_movement_by_id(
    movement_id: UUID,
    use_case: Annotated[GetMovementByIdUseCase, Depends(get_movement_by_id_use_case)],
) -> Any:
    """Get a movement by ID."""
    try:
        dto = GetByIdRequestDTO(id=movement_id)
        movement = await use_case.execute(dto)
        return MovementResponse.model_validate(movement)
    except MovementNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
