from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.core.application.use_cases.commands import (
    ActivateRequestDTO,
    DeactivateRequestDTO,
    DeleteRequestDTO,
)
from src.core.application.use_cases.queries import GetByIdRequestDTO, SearchRequestDTO
from src.core.domain import ConflictError
from src.inventory.application.use_cases.commands import (
    ActivateWarehouseUseCase,
    CreateWarehouseRequestDTO,
    CreateWarehouseUseCase,
    DeactivateWarehouseUseCase,
    DeleteWarehouseUseCase,
    UpdateWarehouseRequestDTO,
    UpdateWarehouseUseCase,
)
from src.inventory.application.use_cases.queries import (
    GetWarehouseByIdUseCase,
    SearchWarehouseUseCase,
)
from src.inventory.domain.exceptions import (
    InvalidWarehouseError,
    WarehouseNotFoundError,
)
from src.inventory.presentation.api import (
    get_activate_warehouse_use_case,
    get_create_warehouse_use_case,
    get_deactivate_warehouse_use_case,
    get_delete_warehouse_use_case,
    get_search_warehouse_use_case,
    get_update_warehouse_use_case,
    get_warehouse_by_id_use_case,
)
from src.inventory.presentation.api.schemas import (
    RegisterWarehouseRequest,
    SearchWarehousesResponse,
    UpdateWarehouseRequest,
    WarehouseResponse,
)

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])


@router.post("", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
async def create_warehouse(
    request: RegisterWarehouseRequest,
    use_case: Annotated[CreateWarehouseUseCase, Depends(get_create_warehouse_use_case)],
) -> Any:
    """Create a new warehouse."""
    try:
        dto = CreateWarehouseRequestDTO(
            name=request.name,
            location_code=request.location_code,
            is_active=request.is_active,
        )
        warehouse = await use_case.execute(dto)
        return WarehouseResponse.model_validate(warehouse)
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except InvalidWarehouseError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.get("", response_model=SearchWarehousesResponse)
async def search_warehouses(
    use_case: Annotated[SearchWarehouseUseCase, Depends(get_search_warehouse_use_case)],
    name: Annotated[str | None, Query(description="Filter by name")] = None,
    location_code: Annotated[
        str | None,
        Query(description="Filter by location code"),
    ] = None,
    is_active: Annotated[
        bool | None,
        Query(description="Filter by active status"),
    ] = None,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
) -> Any:
    """Search warehouses with pagination and filters."""
    filters: dict[str, Any] = {}
    if name is not None:
        filters["name"] = name
    if location_code is not None:
        filters["location_code"] = location_code
    if is_active is not None:
        filters["is_active"] = is_active

    request_dto = SearchRequestDTO(filters=filters, page=page, page_size=page_size)
    response_dto = await use_case.execute(request_dto)
    items = [WarehouseResponse.model_validate(item) for item in response_dto.data]
    return SearchWarehousesResponse(data=items, meta=response_dto.meta)


@router.get("/{warehouse_id}", response_model=WarehouseResponse)
async def get_warehouse_by_id(
    warehouse_id: UUID,
    use_case: Annotated[GetWarehouseByIdUseCase, Depends(get_warehouse_by_id_use_case)],
) -> Any:
    """Get a warehouse by ID."""
    try:
        dto = GetByIdRequestDTO(id=warehouse_id)
        warehouse = await use_case.execute(dto)
        return WarehouseResponse.model_validate(warehouse)
    except WarehouseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put("/{warehouse_id}", response_model=WarehouseResponse)
async def update_warehouse(
    warehouse_id: UUID,
    request: UpdateWarehouseRequest,
    use_case: Annotated[UpdateWarehouseUseCase, Depends(get_update_warehouse_use_case)],
) -> Any:
    """Update an existing warehouse."""
    try:
        dto = UpdateWarehouseRequestDTO(
            id=warehouse_id,
            name=request.name,
            location_code=request.location_code,
        )
        warehouse = await use_case.execute(dto)
        return WarehouseResponse.model_validate(warehouse)
    except WarehouseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidWarehouseError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.delete("/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_warehouse(
    warehouse_id: UUID,
    use_case: Annotated[DeleteWarehouseUseCase, Depends(get_delete_warehouse_use_case)],
) -> None:
    """Delete a warehouse."""
    try:
        dto = DeleteRequestDTO(id=warehouse_id)
        await use_case.execute(dto)
    except WarehouseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put("/{warehouse_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_warehouse(
    warehouse_id: UUID,
    use_case: Annotated[
        ActivateWarehouseUseCase, Depends(get_activate_warehouse_use_case)
    ],
) -> None:
    """Activate a warehouse."""
    try:
        dto = ActivateRequestDTO(id=warehouse_id)
        await use_case.execute(dto)
    except WarehouseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidWarehouseError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.put("/{warehouse_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_warehouse(
    warehouse_id: UUID,
    use_case: Annotated[
        DeactivateWarehouseUseCase, Depends(get_deactivate_warehouse_use_case)
    ],
) -> None:
    """Deactivate a warehouse."""
    try:
        dto = DeactivateRequestDTO(id=warehouse_id)
        await use_case.execute(dto)
    except WarehouseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidWarehouseError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e
