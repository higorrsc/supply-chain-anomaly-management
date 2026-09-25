import pytest
from datetime import datetime, UTC
from uuid import uuid4
from src.inventory.domain.events import MovementCreatedEvent
from src.inventory.domain.enums import MovementType
from src.anomaly.domain.rules import AnomalyRules
from src.anomaly.domain.services.analysis import MovementAnomalyAnalysisService
from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity

@pytest.fixture
def rules():
    return AnomalyRules(
        enabled=True,
        deviation_thresholds={"low": 1.5, "high": 2.5, "critical": 3.5}
    )

def create_event(qty: float):
    return MovementCreatedEvent(
        movement_id=uuid4(),
        item_id=uuid4(),
        warehouse_id=uuid4(),
        quantity_value=str(qty),
        movement_type=MovementType.IN,
        occurrence_date=datetime.now(UTC)
    )

def test_analysis_critical(rules):
    service = MovementAnomalyAnalysisService(rules)
    event = create_event(400.0) # score = 4.0
    severity, score = service.analyze(event)
    assert severity == AnomalySeverity.CRITICAL
    assert score.value == 4.0

def test_analysis_normal(rules):
    service = MovementAnomalyAnalysisService(rules)
    event = create_event(100.0) # score = 1.0
    severity, score = service.analyze(event)
    assert severity is None
    assert score is None

def test_analysis_disabled():
    rules = AnomalyRules(
        enabled=False,
        deviation_thresholds={"low": 1.5, "high": 2.5, "critical": 3.5}
    )
    service = MovementAnomalyAnalysisService(rules)
    event = create_event(1000.0)
    severity, score = service.analyze(event)
    assert severity is None
    assert score is None
