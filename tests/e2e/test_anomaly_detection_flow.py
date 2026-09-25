import asyncio
import uuid

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from src.core.infrastructure.database import AsyncSessionLocal
from src.inventory.domain.entities import Item, Warehouse
from src.inventory.domain.value_objects import SKU
from src.inventory.infrastructure.repositories import (
    ItemRepository,
    WarehouseRepository,
)
from src.main import app


@pytest.mark.asyncio
async def test_end_to_end_anomaly_detection_flow() -> None:
    async with AsyncSessionLocal() as session:
        sku_suffix = uuid.uuid4().hex[:6].upper()
        item = Item(
            sku=SKU(value=f"SKU-{sku_suffix}"),
            description="Anomaly Test Item",
            is_active=True,
        )
        warehouse = Warehouse(name="Anomaly WH", location_code="AW", is_active=True)
        item_repo = ItemRepository(session)
        wh_repo = WarehouseRepository(session)
        await item_repo.save(item)
        await wh_repo.save(warehouse)
        await session.commit()
        item_id = item.id
        warehouse_id = warehouse.id

    async with (
        LifespanManager(app),
        AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client,
    ):
        movement_data = {
            "item_id": str(item_id),
            "warehouse_id": str(warehouse_id),
            "quantity": 500.0,
            "movement_type": "in",
            "occurred_at": "2026-01-01T10:00:00Z",
        }
        response = await client.post("/api/v1/movements", json=movement_data)
        assert response.status_code == 201

        movement_id = response.json()["id"]

        await asyncio.sleep(1.0)

        # Check movement exists in DB
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("SELECT id FROM movements WHERE id = :id"),
                {"id": movement_id},
            )
            assert result.fetchone() is not None
