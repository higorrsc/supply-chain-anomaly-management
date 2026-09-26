import uuid
from datetime import UTC, datetime

from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.rules import (
    AnomalyRules,
    AnomalyThresholds,
    BusinessHoursRule,
    DeviationRule,
    MaxQuantityRule,
    RulesConfig,
)
from src.anomaly.domain.services.evaluators.max_quantity import MaxQuantityEvaluator
from src.inventory.domain.enums import MovementType
from src.inventory.domain.events import MovementCreatedEvent


def create_event(movement_type: str, qty: str) -> MovementCreatedEvent:
    m_type = MovementType.IN if movement_type == "IN" else MovementType.OUT
    return MovementCreatedEvent(
        movement_id=uuid.uuid4(),
        item_id=uuid.uuid4(),
        warehouse_id=uuid.uuid4(),
        movement_type=m_type,
        quantity_value=qty,
        occurrence_date=datetime.now(UTC),
    )


def test_max_quantity_evaluator_within_limits() -> None:
    rules = AnomalyRules(
        enabled=True,
        rules=RulesConfig(
            deviation=DeviationRule(
                thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5)
            ),
            business_hours=BusinessHoursRule(),
            max_quantity=MaxQuantityRule(enabled=True, max_in=100, max_out=50),
        ),
    )
    evaluator = MaxQuantityEvaluator()

    event_in = create_event("IN", "100.0")
    assert evaluator.evaluate(event_in, rules) is None

    event_out = create_event("OUT", "50.0")
    assert evaluator.evaluate(event_out, rules) is None


def test_max_quantity_evaluator_exceeds_limits() -> None:
    rules = AnomalyRules(
        enabled=True,
        rules=RulesConfig(
            deviation=DeviationRule(
                thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5)
            ),
            business_hours=BusinessHoursRule(),
            max_quantity=MaxQuantityRule(enabled=True, max_in=100, max_out=50),
        ),
    )
    evaluator = MaxQuantityEvaluator()

    event_in = create_event("IN", "101.0")
    result_in = evaluator.evaluate(event_in, rules)
    assert result_in is not None
    assert result_in.severity == AnomalySeverity.CRITICAL

    event_out = create_event("OUT", "51.0")
    result_out = evaluator.evaluate(event_out, rules)
    assert result_out is not None
    assert result_out.severity == AnomalySeverity.CRITICAL


def test_max_quantity_evaluator_disabled() -> None:
    rules = AnomalyRules(
        enabled=True,
        rules=RulesConfig(
            deviation=DeviationRule(
                thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5)
            ),
            business_hours=BusinessHoursRule(),
            max_quantity=MaxQuantityRule(enabled=False, max_in=100, max_out=50),
        ),
    )
    evaluator = MaxQuantityEvaluator()

    event_in = create_event("IN", "5000.0")
    assert evaluator.evaluate(event_in, rules) is None
