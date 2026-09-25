from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.core.application.use_cases.queries.generic_search import SearchResponseDTO
from src.core.domain import ConflictError
from src.inventory.application.use_cases.commands import (
    ActivateWarehouseUseCase,
    CreateWarehouseUseCase,
    DeactivateWarehouseUseCase,
    DeleteWarehouseUseCase,
    UpdateWarehouseUseCase,
)
from src.inventory.application.use_cases.queries import (
    GetWarehouseByIdUseCase,
    SearchWarehouseUseCase,
)
from src.inventory.domain.entities import Warehouse
from src.inventory.domain.exceptions import (
    WarehouseNotFoundError,
)
from src.inventory.presentation.api.controllers.warehouse_controller import router
from src.inventory.presentation.api.dependencies import (
    get_activate_warehouse_use_case,
    get_create_warehouse_use_case,
    get_deactivate_warehouse_use_case,
    get_delete_warehouse_use_case,
    get_search_warehouse_use_case,
    get_update_warehouse_use_case,
    get_warehouse_by_id_use_case,
)

app = FastAPI()
app.include_router(router)

mock_create_uc = AsyncMock(spec=CreateWarehouseUseCase)
mock_get_by_id_uc = AsyncMock(spec=GetWarehouseByIdUseCase)
mock_search_uc = AsyncMock(spec=SearchWarehouseUseCase)
mock_update_uc = AsyncMock(spec=UpdateWarehouseUseCase)
mock_delete_uc = AsyncMock(spec=DeleteWarehouseUseCase)
mock_activate_uc = AsyncMock(spec=ActivateWarehouseUseCase)
mock_deactivate_uc = AsyncMock(spec=DeactivateWarehouseUseCase)

app.dependency_overrides[get_create_warehouse_use_case] = lambda: mock_create_uc
app.dependency_overrides[get_warehouse_by_id_use_case] = lambda: mock_get_by_id_uc
app.dependency_overrides[get_search_warehouse_use_case] = lambda: mock_search_uc
app.dependency_overrides[get_update_warehouse_use_case] = lambda: mock_update_uc
app.dependency_overrides[get_delete_warehouse_use_case] = lambda: mock_delete_uc
app.dependency_overrides[get_activate_warehouse_use_case] = lambda: mock_activate_uc
app.dependency_overrides[get_deactivate_warehouse_use_case] = lambda: mock_deactivate_uc


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


class TestWarehouseController:
    @pytest.mark.asyncio
    async def test_create_warehouse(self, client: AsyncClient) -> None:
        warehouse = Warehouse(
            name="Main Warehouse",
            location_code="WH-01",
            is_active=True,
        )
        mock_create_uc.execute.return_value = warehouse
        response = await client.post(
            "/warehouses",
            json={"name": "Main Warehouse", "location_code": "WH-01"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == str(warehouse.id)
        assert data["name"] == "Main Warehouse"

    @pytest.mark.asyncio
    async def test_create_warehouse_conflict(self, client: AsyncClient) -> None:
        mock_create_uc.execute.side_effect = ConflictError("Exists")
        response = await client.post(
            "/warehouses",
            json={"name": "Main Warehouse", "location_code": "WH-01"},
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_get_warehouse_by_id(self, client: AsyncClient) -> None:
        warehouse = Warehouse(
            name="Main Warehouse",
            location_code="WH-01",
            is_active=True,
        )
        mock_get_by_id_uc.execute.return_value = warehouse
        response = await client.get(f"/warehouses/{warehouse.id}")
        assert response.status_code == 200
        assert response.json()["id"] == str(warehouse.id)

    @pytest.mark.asyncio
    async def test_get_warehouse_not_found(self, client: AsyncClient) -> None:
        mock_get_by_id_uc.execute.side_effect = WarehouseNotFoundError(uuid4())
        response = await client.get(f"/warehouses/{uuid4()}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_warehouse(self, client: AsyncClient) -> None:
        warehouse = Warehouse(
            name="Updated Warehouse",
            location_code="WH-02",
            is_active=True,
        )
        mock_update_uc.execute.return_value = warehouse
        response = await client.put(
            f"/warehouses/{warehouse.id}",
            json={"name": "Updated Warehouse", "location_code": "WH-02"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Warehouse"

    @pytest.mark.asyncio
    async def test_delete_warehouse(self, client: AsyncClient) -> None:
        mock_delete_uc.execute.return_value = None
        response = await client.delete(f"/warehouses/{uuid4()}")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_activate_warehouse(self, client: AsyncClient) -> None:
        mock_activate_uc.execute.return_value = None
        response = await client.put(f"/warehouses/{uuid4()}/activate")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_deactivate_warehouse(self, client: AsyncClient) -> None:
        mock_deactivate_uc.execute.return_value = None
        response = await client.put(f"/warehouses/{uuid4()}/deactivate")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_search_warehouses(self, client: AsyncClient) -> None:
        warehouse = Warehouse(
            name="Main Warehouse",
            location_code="WH-01",
            is_active=True,
        )
        page_response = SearchResponseDTO(
            data=[warehouse],
            meta={"total_items": 1, "page": 1, "page_size": 10, "total_pages": 1},
        )
        mock_search_uc.execute.return_value = page_response

        response = await client.get("/warehouses?is_active=true")
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["total_items"] == 1
        assert len(data["data"]) == 1
