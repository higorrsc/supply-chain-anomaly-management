from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.infrastructure.database.session import get_db_session
from src.inventory.application.use_cases.commands import (
    ActivateItemUseCase,
    ActivateWarehouseUseCase,
    CreateItemUseCase,
    CreateMovementUseCase,
    CreateWarehouseUseCase,
    DeactivateItemUseCase,
    DeactivateWarehouseUseCase,
    DeleteItemUseCase,
    DeleteWarehouseUseCase,
    UpdateItemUseCase,
    UpdateWarehouseUseCase,
)
from src.inventory.application.use_cases.queries import (
    GetItemByIdUseCase,
    GetItemBySKUUseCase,
    GetMovementByIdUseCase,
    GetWarehouseByIdUseCase,
    SearchItemUseCase,
    SearchMovementUseCase,
    SearchWarehouseUseCase,
)
from src.inventory.infrastructure.repositories import (
    ItemRepository,
    MovementRepository,
    WarehouseRepository,
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


# Repositories
def get_item_repository(session: SessionDep) -> ItemRepository:
    return ItemRepository(session=session)


def get_warehouse_repository(session: SessionDep) -> WarehouseRepository:
    return WarehouseRepository(session=session)


def get_movement_repository(session: SessionDep) -> MovementRepository:
    return MovementRepository(session=session)


ItemRepoDep = Annotated[ItemRepository, Depends(get_item_repository)]
WarehouseRepoDep = Annotated[WarehouseRepository, Depends(get_warehouse_repository)]
MovementRepoDep = Annotated[MovementRepository, Depends(get_movement_repository)]


# Item Use Cases
def get_create_item_use_case(repo: ItemRepoDep) -> CreateItemUseCase:
    return CreateItemUseCase(repository=repo)


def get_update_item_use_case(repo: ItemRepoDep) -> UpdateItemUseCase:
    return UpdateItemUseCase(repository=repo)


def get_delete_item_use_case(repo: ItemRepoDep) -> DeleteItemUseCase:
    return DeleteItemUseCase(repository=repo)


def get_activate_item_use_case(repo: ItemRepoDep) -> ActivateItemUseCase:
    return ActivateItemUseCase(repository=repo)


def get_deactivate_item_use_case(repo: ItemRepoDep) -> DeactivateItemUseCase:
    return DeactivateItemUseCase(repository=repo)


def get_item_by_id_use_case(repo: ItemRepoDep) -> GetItemByIdUseCase:
    return GetItemByIdUseCase(repository=repo)


def get_item_by_sku_use_case(repo: ItemRepoDep) -> GetItemBySKUUseCase:
    from src.inventory.domain.exceptions import ItemNotFoundError

    return GetItemBySKUUseCase(repository=repo, not_found_exception=ItemNotFoundError)


def get_search_item_use_case(repo: ItemRepoDep) -> SearchItemUseCase:
    return SearchItemUseCase(repository=repo)


# Warehouse Use Cases
def get_create_warehouse_use_case(repo: WarehouseRepoDep) -> CreateWarehouseUseCase:
    return CreateWarehouseUseCase(repository=repo)


def get_update_warehouse_use_case(repo: WarehouseRepoDep) -> UpdateWarehouseUseCase:
    return UpdateWarehouseUseCase(repository=repo)


def get_delete_warehouse_use_case(repo: WarehouseRepoDep) -> DeleteWarehouseUseCase:
    return DeleteWarehouseUseCase(repository=repo)


def get_activate_warehouse_use_case(repo: WarehouseRepoDep) -> ActivateWarehouseUseCase:
    return ActivateWarehouseUseCase(repository=repo)


def get_deactivate_warehouse_use_case(
    repo: WarehouseRepoDep,
) -> DeactivateWarehouseUseCase:
    return DeactivateWarehouseUseCase(repository=repo)


def get_warehouse_by_id_use_case(repo: WarehouseRepoDep) -> GetWarehouseByIdUseCase:
    return GetWarehouseByIdUseCase(repository=repo)


def get_search_warehouse_use_case(repo: WarehouseRepoDep) -> SearchWarehouseUseCase:
    return SearchWarehouseUseCase(repository=repo)


# Movement Use Cases
def get_create_movement_use_case(
    repo: MovementRepoDep, item_repo: ItemRepoDep, warehouse_repo: WarehouseRepoDep
) -> CreateMovementUseCase:
    return CreateMovementUseCase(
        repository=repo, item_repository=item_repo, warehouse_repository=warehouse_repo
    )


def get_movement_by_id_use_case(repo: MovementRepoDep) -> GetMovementByIdUseCase:
    return GetMovementByIdUseCase(repository=repo)


def get_search_movement_use_case(repo: MovementRepoDep) -> SearchMovementUseCase:
    return SearchMovementUseCase(repository=repo)
