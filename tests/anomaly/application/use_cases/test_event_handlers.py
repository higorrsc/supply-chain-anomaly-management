import pytest
from datetime import datetime, UTC
from uuid import uuid4
from src.inventory.domain.events import MovementCreatedEvent
from src.inventory.domain.enums import MovementType
from src.anomaly.domain.rules import AnomalyRules
from src.anomaly.application.use_cases.event_handlers import DetectAnomalyForMovementHandler
from tests.fakes.repositories import FakeAnomalyRepository
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity

@pytest.mark.asyncio
async def test_detect_anomaly_handler():
    repo = FakeAnomalyRepository()
    rules = AnomalyRules(
        enabled=True,
        deviation_thresholds={"low": 1.5, "high": 2.5, "critical": 3.5}
    )
    handler = DetectAnomalyForMovementHandler(repository=repo, rules=rules)
    
    event = MovementCreatedEvent(
        movement_id=uuid4(),
        item_id=uuid4(),
        warehouse_id=uuid4(),
        quantity_value="400.0",
        movement_type=MovementType.IN,
        occurrence_date=datetime.now(UTC)
    )
    
    await handler.handle(event)
    
    # Verify anomaly was created
    anomalies = repo._data.values()
    assert len(anomalies) == 1
    anomaly = list(anomalies)[0]
    assert anomaly.item_id == event.item_id
    assert anomaly.severity == AnomalySeverity.CRITICAL

@pytest.mark.asyncio
async def test_detect_anomaly_handler_no_anomaly():
    repo = FakeAnomalyRepository()
    rules = AnomalyRules(
        enabled=True,
        deviation_thresholds={"low": 1.5, "high": 2.5, "critical": 3.5}
    )
    handler = DetectAnomalyForMovementHandler(repository=repo, rules=rules)
    
    event = MovementCreatedEvent(
        movement_id=uuid4(),
        item_id=uuid4(),
        warehouse_id=uuid4(),
        quantity_value="100.0",
        movement_type=MovementType.IN,
        occurrence_date=datetime.now(UTC)
    )
    
    await handler.handle(event)
    
    # Verify no anomaly was created
    assert len(repo._data) == 0
