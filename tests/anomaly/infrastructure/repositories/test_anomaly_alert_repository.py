from datetime import UTC, datetime
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.anomaly.domain.entities.anomaly import Anomaly
from src.anomaly.domain.entities.anomaly_alert import AnomalyAlert
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.enums.anomaly_status import AnomalyStatus
from src.anomaly.domain.value_objects.score import Score
from src.anomaly.infrastructure.repositories.anomaly_alert_repository import (
    AnomalyAlertRepository,
)
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


class TestAnomalyAlertRepository:
    """Test suite for AnomalyAlertRepository using an in-memory database."""

    @pytest.mark.asyncio
    async def test_save_and_get_by_id(self, db_session: AsyncSession) -> None:
        """Test saving and retrieving an anomaly alert."""

        # Setup FKs
        item = Item(sku=SKU(value="TEST-ALRT1"), description="Test", is_active=True)
        warehouse = Warehouse(name="W1", location_code="L1", is_active=True)
        await ItemRepository(session=db_session).save(item)
        await WarehouseRepository(session=db_session).save(warehouse)

        movement = Movement(
            item_id=item.id,
            warehouse_id=warehouse.id,
            quantity=Quantity(value=Decimal("10.0")),
            movement_type=MovementType.IN,
            occurred_at=datetime.now(UTC),
        )
        await MovementRepository(session=db_session).save(movement)

        anomaly = Anomaly(
            movement_id=movement.id,
            item_id=item.id,
            score=Score(value=Decimal("99.0")),
            severity=AnomalySeverity.CRITICAL,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )
        await AnomalyRepository(session=db_session).save(anomaly)

        repository = AnomalyAlertRepository(session=db_session)
        alert = AnomalyAlert(
            anomaly_id=anomaly.id,
            message="Critical Anomaly Detected",
            is_read=False,
            generated_at=datetime.now(UTC),
        )

        saved = await repository.save(alert)
        assert saved is not None
        assert saved.id is not None
        assert saved.message == "Critical Anomaly Detected"

        retrieved = await repository.get_by_id(saved.id)
        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.message == "Critical Anomaly Detected"

    @pytest.mark.asyncio
    async def test_get_by_anomaly_id(self, db_session: AsyncSession) -> None:
        """Test retrieving alerts by anomaly ID."""

        # Setup FKs
        item = Item(sku=SKU(value="TEST-ALRT2"), description="Test", is_active=True)
        warehouse = Warehouse(name="W2", location_code="L2", is_active=True)
        await ItemRepository(session=db_session).save(item)
        await WarehouseRepository(session=db_session).save(warehouse)

        movement = Movement(
            item_id=item.id,
            warehouse_id=warehouse.id,
            quantity=Quantity(value=Decimal("5.0")),
            movement_type=MovementType.OUT,
            occurred_at=datetime.now(UTC),
        )
        await MovementRepository(session=db_session).save(movement)

        anomaly = Anomaly(
            movement_id=movement.id,
            item_id=item.id,
            score=Score(value=Decimal("95.0")),
            severity=AnomalySeverity.CRITICAL,
            status=AnomalyStatus.OPEN,
            detected_at=datetime.now(UTC),
        )
        await AnomalyRepository(session=db_session).save(anomaly)

        repository = AnomalyAlertRepository(session=db_session)
        alert1 = AnomalyAlert(
            anomaly_id=anomaly.id,
            message="Alert 1",
            is_read=False,
            generated_at=datetime.now(UTC),
        )
        alert2 = AnomalyAlert(
            anomaly_id=anomaly.id,
            message="Alert 2",
            is_read=True,
            generated_at=datetime.now(UTC),
        )
        await repository.save(alert1)
        await repository.save(alert2)

        retrieved_alerts = await repository.get_by_anomaly_id(anomaly.id)
        assert len(retrieved_alerts) == 2
        assert any(a.message == "Alert 1" for a in retrieved_alerts)
        assert any(a.message == "Alert 2" for a in retrieved_alerts)
