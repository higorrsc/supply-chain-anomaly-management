from datetime import UTC, datetime
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.value_objects.score import Score
from src.anomaly.infrastructure.repositories.anomaly_repository import AnomalyRepository
from src.inventory.domain.entities.item import Item
from src.inventory.domain.entities.movement import Movement
from src.inventory.domain.entities.warehouse import Warehouse
from src.inventory.domain.enums.movement_type import MovementType
from src.inventory.domain.value_objects.quantity import Quantity
from src.inventory.domain.value_objects.sku import SKU
from src.inventory.infrastructure.repositories.item_repository import ItemRepository
from src.inventory.infrastructure.repositories.movement_repository import (
    MovementRepository,
)
from src.inventory.infrastructure.repositories.warehouse_repository import (
    WarehouseRepository,
)


class TestAnomalyRepository:
    """Test suite for AnomalyRepository using an in-memory database."""

    @pytest.mark.asyncio
    async def test_save_and_get_by_id(self, db_session: AsyncSession) -> None:
        """Test saving and retrieving an anomaly."""

        # Need to create Item, Warehouse, and Movement to satisfy FKs
        item_repo = ItemRepository(session=db_session)
        warehouse_repo = WarehouseRepository(session=db_session)
        movement_repo = MovementRepository(session=db_session)

        item = Item(sku=SKU(value="TEST-SKU01"), description="Test", is_active=True)
        warehouse = Warehouse(name="W1", location_code="L1", is_active=True)
        await item_repo.save(item)
        await warehouse_repo.save(warehouse)

        movement = Movement(
            item_id=item.id,
            warehouse_id=warehouse.id,
            quantity=Quantity(value=Decimal("10.0")),
            movement_type=MovementType.IN,
            occurred_at=datetime.now(UTC),
        )
        await movement_repo.save(movement)

        repository = AnomalyRepository(session=db_session)

        anomaly = Anomaly(
            movement_id=movement.id,
            item_id=item.id,
            score=Score(value=Decimal("95.0")),
            severity=AnomalySeverity.CRITICAL,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )

        saved_anomaly = await repository.save(anomaly)
        assert saved_anomaly is not None
        assert saved_anomaly.id is not None
        assert saved_anomaly.severity == AnomalySeverity.CRITICAL

        retrieved = await repository.get_by_id(saved_anomaly.id)
        assert retrieved is not None
        assert retrieved.id == saved_anomaly.id
        assert retrieved.score.value == Decimal("95.0")

    @pytest.mark.asyncio
    async def test_update_anomaly(self, db_session: AsyncSession) -> None:
        """Test updating an existing anomaly."""

        item_repo = ItemRepository(session=db_session)
        warehouse_repo = WarehouseRepository(session=db_session)
        movement_repo = MovementRepository(session=db_session)

        item = Item(sku=SKU(value="TEST-SKU02"), description="Test", is_active=True)
        warehouse = Warehouse(name="W2", location_code="L2", is_active=True)
        await item_repo.save(item)
        await warehouse_repo.save(warehouse)

        movement = Movement(
            item_id=item.id,
            warehouse_id=warehouse.id,
            quantity=Quantity(value=Decimal("5.0")),
            movement_type=MovementType.OUT,
            occurred_at=datetime.now(UTC),
        )
        await movement_repo.save(movement)

        repository = AnomalyRepository(session=db_session)
        anomaly = Anomaly(
            movement_id=movement.id,
            item_id=item.id,
            score=Score(value=Decimal("80.0")),
            severity=AnomalySeverity.HIGH,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )
        saved = await repository.save(anomaly)

        saved.resolve()

        updated = await repository.update(saved)
        assert updated.status == AnomalyStatus.RESOLVED

        retrieved = await repository.get_by_id(saved.id)
        assert retrieved is not None
        assert retrieved.status == AnomalyStatus.RESOLVED

    @pytest.mark.asyncio
    async def test_delete_anomaly(self, db_session: AsyncSession) -> None:
        """Test deleting an anomaly."""

        item_repo = ItemRepository(session=db_session)
        warehouse_repo = WarehouseRepository(session=db_session)
        movement_repo = MovementRepository(session=db_session)

        item = Item(sku=SKU(value="TEST-SKU03"), description="Test", is_active=True)
        warehouse = Warehouse(name="W3", location_code="L3", is_active=True)
        await item_repo.save(item)
        await warehouse_repo.save(warehouse)

        movement = Movement(
            item_id=item.id,
            warehouse_id=warehouse.id,
            quantity=Quantity(value=Decimal("5.0")),
            movement_type=MovementType.OUT,
            occurred_at=datetime.now(UTC),
        )
        await movement_repo.save(movement)

        repository = AnomalyRepository(session=db_session)
        anomaly = Anomaly(
            movement_id=movement.id,
            item_id=item.id,
            score=Score(value=Decimal("70.0")),
            severity=AnomalySeverity.MEDIUM,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )
        saved = await repository.save(anomaly)

        await repository.delete(saved.id)

        retrieved = await repository.get_by_id(saved.id)
        assert retrieved is None
