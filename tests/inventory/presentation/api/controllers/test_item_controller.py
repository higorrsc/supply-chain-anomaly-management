from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.core.application.use_cases.queries import SearchResponseDTO
from src.core.domain.exceptions import (
    ConflictError,
    DomainError,
    EntityNotFoundError,
    EntityValidationError,
)
from src.inventory.application.use_cases.commands import (
    ActivateItemUseCase,
    CreateItemUseCase,
    DeactivateItemUseCase,
    DeleteItemUseCase,
    UpdateItemUseCase,
)
from src.inventory.application.use_cases.queries import (
    GetItemByIdUseCase,
    GetItemBySKUUseCase,
    SearchItemUseCase,
)
from src.inventory.domain.entities import Item
from src.inventory.domain.exceptions import ItemNotFoundError
from src.inventory.domain.value_objects import SKU
from src.inventory.presentation.api.controllers import item_router
from src.inventory.presentation.api.dependencies import (
    get_activate_item_use_case,
    get_create_item_use_case,
    get_deactivate_item_use_case,
    get_delete_item_use_case,
    get_item_by_id_use_case,
    get_item_by_sku_use_case,
    get_search_item_use_case,
    get_update_item_use_case,
)
from src.main import (
    conflict_error_handler,
    domain_error_handler,
    entity_not_found_handler,
    entity_validation_error_handler,
)

app = FastAPI()
app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)  # type: ignore[arg-type]
app.add_exception_handler(ConflictError, conflict_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(EntityValidationError, entity_validation_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(DomainError, domain_error_handler)  # type: ignore[arg-type]

app.include_router(item_router)

mock_create_uc = AsyncMock(spec=CreateItemUseCase)
mock_get_by_id_uc = AsyncMock(spec=GetItemByIdUseCase)
mock_get_by_sku_uc = AsyncMock(spec=GetItemBySKUUseCase)
mock_search_uc = AsyncMock(spec=SearchItemUseCase)
mock_update_uc = AsyncMock(spec=UpdateItemUseCase)
mock_delete_uc = AsyncMock(spec=DeleteItemUseCase)
mock_activate_uc = AsyncMock(spec=ActivateItemUseCase)
mock_deactivate_uc = AsyncMock(spec=DeactivateItemUseCase)

app.dependency_overrides[get_create_item_use_case] = lambda: mock_create_uc
app.dependency_overrides[get_item_by_id_use_case] = lambda: mock_get_by_id_uc
app.dependency_overrides[get_item_by_sku_use_case] = lambda: mock_get_by_sku_uc
app.dependency_overrides[get_search_item_use_case] = lambda: mock_search_uc
app.dependency_overrides[get_update_item_use_case] = lambda: mock_update_uc
app.dependency_overrides[get_delete_item_use_case] = lambda: mock_delete_uc
app.dependency_overrides[get_activate_item_use_case] = lambda: mock_activate_uc
app.dependency_overrides[get_deactivate_item_use_case] = lambda: mock_deactivate_uc


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


class TestItemController:
    @pytest.mark.asyncio
    async def test_create_item(self, client: AsyncClient) -> None:
        item = Item(
            sku=SKU(value="TEST-123"),
            description="Test item",
            is_active=True,
        )
        mock_create_uc.execute.return_value = item
        response = await client.post(
            "/items", json={"sku": "TEST-123", "description": "Test item"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == str(item.id)
        assert data["sku"] == "TEST-123"

    @pytest.mark.asyncio
    async def test_create_item_conflict(self, client: AsyncClient) -> None:
        mock_create_uc.execute.side_effect = ConflictError("Exists")
        response = await client.post(
            "/items", json={"sku": "TEST-123", "description": "Test item"}
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_get_item_by_id_success(self, client: AsyncClient) -> None:
        item = Item(
            sku=SKU(value="TEST-123"),
            description="Test item",
            is_active=True,
        )
        mock_get_by_id_uc.execute.return_value = item
        response = await client.get(f"/items/{item.id}")
        assert response.status_code == 200
        assert response.json()["id"] == str(item.id)

    @pytest.mark.asyncio
    async def test_get_item_by_id_not_found(self, client: AsyncClient) -> None:
        mock_get_by_id_uc.execute.side_effect = ItemNotFoundError(uuid4())
        response = await client.get(f"/items/{uuid4()}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_item(self, client: AsyncClient) -> None:
        item = Item(
            sku=SKU(value="TEST-123"),
            description="Updated item",
            is_active=True,
        )
        mock_update_uc.execute.return_value = item
        response = await client.put(
            f"/items/{item.id}", json={"description": "Updated item"}
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Updated item"

    @pytest.mark.asyncio
    async def test_delete_item(self, client: AsyncClient) -> None:
        mock_delete_uc.execute.return_value = None
        response = await client.delete(f"/items/{uuid4()}")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_activate_item(self, client: AsyncClient) -> None:
        mock_activate_uc.execute.return_value = None
        response = await client.put(f"/items/{uuid4()}/activate")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_deactivate_item(self, client: AsyncClient) -> None:
        mock_deactivate_uc.execute.return_value = None
        response = await client.put(f"/items/{uuid4()}/deactivate")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_search_items(self, client: AsyncClient) -> None:
        item = Item(
            sku=SKU(value="TEST-123"),
            description="Test item",
            is_active=True,
        )
        page_response = SearchResponseDTO(
            data=[item],
            meta={"total_items": 1, "page": 1, "page_size": 10, "total_pages": 1},
        )
        mock_search_uc.execute.return_value = page_response

        response = await client.get("/items?sku=TEST-123")
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["total_items"] == 1
        assert len(data["data"]) == 1
