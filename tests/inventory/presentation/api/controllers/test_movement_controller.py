from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.core.application.use_cases.queries.generic_search import SearchResponseDTO
from src.inventory.application.use_cases.commands import CreateMovementUseCase
from src.inventory.application.use_cases.queries import (
    GetMovementByIdUseCase,
    SearchMovementUseCase,
)
from src.inventory.domain.entities import Movement
from src.inventory.domain.enums import MovementType
from src.inventory.domain.exceptions import MovementNotFoundError
from src.inventory.domain.value_objects import Quantity
from src.inventory.presentation.api.controllers.movement_controller import router
from src.inventory.presentation.api.dependencies import (
    get_create_movement_use_case,
    get_movement_by_id_use_case,
    get_search_movement_use_case,
)

app = FastAPI()
app.include_router(router)

mock_create_uc = AsyncMock(spec=CreateMovementUseCase)
mock_get_by_id_uc = AsyncMock(spec=GetMovementByIdUseCase)
mock_search_uc = AsyncMock(spec=SearchMovementUseCase)

app.dependency_overrides[get_create_movement_use_case] = lambda: mock_create_uc
app.dependency_overrides[get_movement_by_id_use_case] = lambda: mock_get_by_id_uc
app.dependency_overrides[get_search_movement_use_case] = lambda: mock_search_uc


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


class TestMovementController:
    @pytest.mark.asyncio
    async def test_create_movement(self, client: AsyncClient) -> None:
        item_id = uuid4()
        warehouse_id = uuid4()
        now = datetime.now(UTC)
        movement = Movement(
            item_id=item_id,
            warehouse_id=warehouse_id,
            quantity=Quantity(value=Decimal("10.5")),
            movement_type=MovementType.IN,
            occurred_at=now,
        )
        mock_create_uc.execute.return_value = movement

        payload = {
            "item_id": str(item_id),
            "warehouse_id": str(warehouse_id),
            "quantity": 10.5,
            "movement_type": "in",
            "occurred_at": now.isoformat(),
        }

        response = await client.post("/movements", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == str(movement.id)
        assert data["quantity"] == "10.5"
        assert data["movement_type"] == "in"

    @pytest.mark.asyncio
    async def test_get_movement_by_id(self, client: AsyncClient) -> None:
        movement = Movement(
            item_id=uuid4(),
            warehouse_id=uuid4(),
            quantity=Quantity(value=Decimal("10.5")),
            movement_type=MovementType.IN,
            occurred_at=datetime.now(UTC),
        )
        mock_get_by_id_uc.execute.return_value = movement

        response = await client.get(f"/movements/{movement.id}")
        assert response.status_code == 200
        assert response.json()["id"] == str(movement.id)

    @pytest.mark.asyncio
    async def test_get_movement_not_found(self, client: AsyncClient) -> None:
        mock_get_by_id_uc.execute.side_effect = MovementNotFoundError(uuid4())
        response = await client.get(f"/movements/{uuid4()}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_search_movements(self, client: AsyncClient) -> None:
        movement = Movement(
            item_id=uuid4(),
            warehouse_id=uuid4(),
            quantity=Quantity(value=Decimal("10.5")),
            movement_type=MovementType.IN,
            occurred_at=datetime.now(UTC),
        )
        page_response = SearchResponseDTO(
            data=[movement],
            meta={"total_items": 1, "page": 1, "page_size": 10, "total_pages": 1},
        )
        mock_search_uc.execute.return_value = page_response

        response = await client.get("/movements?movement_type=in")
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["total_items"] == 1
        assert len(data["data"]) == 1
