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
    ActivateItemUseCase,
    CreateItemRequestDTO,
    CreateItemUseCase,
    DeactivateItemUseCase,
    DeleteItemUseCase,
    UpdateItemRequestDTO,
    UpdateItemUseCase,
)
from src.inventory.application.use_cases.queries import (
    GetItemByIdUseCase,
    GetItemBySKURequestDTO,
    GetItemBySKUUseCase,
    SearchItemUseCase,
)
from src.inventory.domain.exceptions import InvalidItemError, ItemNotFoundError
from src.inventory.domain.value_objects import SKU
from src.inventory.presentation.api import (
    get_activate_item_use_case,
    get_create_item_use_case,
    get_deactivate_item_use_case,
    get_delete_item_use_case,
    get_item_by_id_use_case,
    get_item_by_sku_use_case,
    get_search_item_use_case,
    get_update_item_use_case,
)
from src.inventory.presentation.api.schemas import (
    ItemResponse,
    RegisterItemRequest,
    SearchItemsResponse,
    UpdateItemRequest,
)

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    request: RegisterItemRequest,
    use_case: Annotated[CreateItemUseCase, Depends(get_create_item_use_case)],
) -> Any:
    """Create a new item."""
    try:
        dto = CreateItemRequestDTO(
            sku=request.sku,
            description=request.description,
            is_active=request.is_active,
        )
        item = await use_case.execute(dto)
        return ItemResponse.model_validate(item)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except InvalidItemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e


@router.get("", response_model=SearchItemsResponse)
async def search_items(
    use_case: Annotated[SearchItemUseCase, Depends(get_search_item_use_case)],
    sku: Annotated[str | None, Query(description="Filter by SKU")] = None,
    description: Annotated[
        str | None, Query(description="Filter by description")
    ] = None,
    is_active: Annotated[
        bool | None, Query(description="Filter by active status")
    ] = None,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
) -> Any:
    """Search items with pagination and filters."""
    filters: dict[str, Any] = {}
    if sku is not None:
        filters["sku"] = sku
    if description is not None:
        filters["description"] = description
    if is_active is not None:
        filters["is_active"] = is_active

    request_dto = SearchRequestDTO(filters=filters, page=page, page_size=page_size)
    response_dto = await use_case.execute(request_dto)
    items = [ItemResponse.model_validate(item) for item in response_dto.data]
    return SearchItemsResponse(data=items, meta=response_dto.meta)


@router.get("/sku/{sku}", response_model=ItemResponse)
async def get_item_by_sku(
    sku: str,
    use_case: Annotated[GetItemBySKUUseCase, Depends(get_item_by_sku_use_case)],
) -> Any:
    """Get an item by SKU."""
    try:
        dto = GetItemBySKURequestDTO(sku=SKU(value=sku))
        item = await use_case.execute(dto)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with SKU {sku} not found",
            )
        return ItemResponse.model_validate(item)
    except InvalidItemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item_by_id(
    item_id: UUID,
    use_case: Annotated[GetItemByIdUseCase, Depends(get_item_by_id_use_case)],
) -> Any:
    """Get an item by ID."""
    try:
        dto = GetByIdRequestDTO(id=item_id)
        item = await use_case.execute(dto)
        return ItemResponse.model_validate(item)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: UUID,
    request: UpdateItemRequest,
    use_case: Annotated[UpdateItemUseCase, Depends(get_update_item_use_case)],
) -> Any:
    """Update an existing item."""
    try:
        dto = UpdateItemRequestDTO(
            id=item_id,
            description=request.description,
        )
        item = await use_case.execute(dto)
        return ItemResponse.model_validate(item)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InvalidItemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID,
    use_case: Annotated[DeleteItemUseCase, Depends(get_delete_item_use_case)],
) -> None:
    """Delete an item."""
    try:
        dto = DeleteRequestDTO(id=item_id)
        await use_case.execute(dto)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.put("/{item_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_item(
    item_id: UUID,
    use_case: Annotated[ActivateItemUseCase, Depends(get_activate_item_use_case)],
) -> None:
    """Activate an item."""
    try:
        dto = ActivateRequestDTO(id=item_id)
        await use_case.execute(dto)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InvalidItemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e


@router.put("/{item_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_item(
    item_id: UUID,
    use_case: Annotated[DeactivateItemUseCase, Depends(get_deactivate_item_use_case)],
) -> None:
    """Deactivate an item."""
    try:
        dto = DeactivateRequestDTO(id=item_id)
        await use_case.execute(dto)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InvalidItemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        ) from e
