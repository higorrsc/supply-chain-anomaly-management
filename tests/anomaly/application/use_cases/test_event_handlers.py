from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.anomaly.application.use_cases.event_handlers import (
    DetectAnomalyForMovementHandler,
)
from src.anomaly.domain.enums import AnomalySeverity
from src.anomaly.domain.rules import AnomalyRules, AnomalyThresholds
from src.inventory.domain.enums import MovementType
from src.inventory.domain.events import MovementCreatedEvent
from tests.fakes.repositories import FakeAnomalyRepository


@pytest.mark.asyncio
async def test_detect_anomaly_handler() -> None:
    repo = FakeAnomalyRepository()
    rules = AnomalyRules(
        enabled=True,
        deviation_thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5),
    )
    handler = DetectAnomalyForMovementHandler(repository=repo, rules=rules)

    event = MovementCreatedEvent(
        movement_id=uuid4(),
        item_id=uuid4(),
        warehouse_id=uuid4(),
        quantity_value="400.0",
        movement_type=MovementType.IN,
        occurrence_date=datetime.now(UTC),
    )

    await handler.handle(event)

    # Verify anomaly was created
    anomalies = repo._data.values()
    assert len(anomalies) == 1
    anomaly = next(iter(anomalies))
    assert anomaly.item_id == event.item_id
    assert anomaly.severity == AnomalySeverity.CRITICAL


@pytest.mark.asyncio
async def test_detect_anomaly_handler_no_anomaly() -> None:
    repo = FakeAnomalyRepository()
    rules = AnomalyRules(
        enabled=True,
        deviation_thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5),
    )
    handler = DetectAnomalyForMovementHandler(repository=repo, rules=rules)

    event = MovementCreatedEvent(
        movement_id=uuid4(),
        item_id=uuid4(),
        warehouse_id=uuid4(),
        quantity_value="100.0",
        movement_type=MovementType.IN,
        occurrence_date=datetime.now(UTC),
    )

    await handler.handle(event)

    # Verify no anomaly was created
    assert len(repo._data) == 0
