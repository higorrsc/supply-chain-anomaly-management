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
from src.anomaly.domain.services.evaluators.business_hours import BusinessHoursEvaluator
from src.inventory.domain.enums import MovementType
from src.inventory.domain.events import MovementCreatedEvent


def create_event(hour: int, minute: int) -> MovementCreatedEvent:
    now = datetime.now(UTC)
    occurred_at = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return MovementCreatedEvent(
        movement_id=uuid.uuid4(),
        item_id=uuid.uuid4(),
        warehouse_id=uuid.uuid4(),
        movement_type=MovementType.IN,
        quantity_value="100.0",
        occurrence_date=occurred_at,
    )


def test_business_hours_evaluator_within_hours() -> None:
    rules = AnomalyRules(
        enabled=True,
        rules=RulesConfig(
            deviation=DeviationRule(
                thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5)
            ),
            business_hours=BusinessHoursRule(
                enabled=True, start_time="08:00", end_time="18:00"
            ),
            max_quantity=MaxQuantityRule(),
        ),
    )
    evaluator = BusinessHoursEvaluator()

    # Inside business hours
    event = create_event(hour=10, minute=30)
    result = evaluator.evaluate(event, rules)
    assert result is None


def test_business_hours_evaluator_outside_hours() -> None:
    rules = AnomalyRules(
        enabled=True,
        rules=RulesConfig(
            deviation=DeviationRule(
                thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5)
            ),
            business_hours=BusinessHoursRule(
                enabled=True, start_time="08:00", end_time="18:00"
            ),
            max_quantity=MaxQuantityRule(),
        ),
    )
    evaluator = BusinessHoursEvaluator()

    # Outside business hours (early)
    event = create_event(hour=7, minute=59)
    result = evaluator.evaluate(event, rules)
    assert result is not None
    assert result.severity == AnomalySeverity.HIGH
    assert result.score == 50.0

    # Outside business hours (late)
    event2 = create_event(hour=18, minute=1)
    result2 = evaluator.evaluate(event2, rules)
    assert result2 is not None
    assert result2.severity == AnomalySeverity.HIGH
    assert result2.score == 50.0


def test_business_hours_evaluator_disabled() -> None:
    rules = AnomalyRules(
        enabled=True,
        rules=RulesConfig(
            deviation=DeviationRule(
                thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5)
            ),
            business_hours=BusinessHoursRule(
                enabled=False, start_time="08:00", end_time="18:00"
            ),
            max_quantity=MaxQuantityRule(),
        ),
    )
    evaluator = BusinessHoursEvaluator()

    # Outside business hours but rule disabled
    event = create_event(hour=23, minute=0)
    result = evaluator.evaluate(event, rules)
    assert result is None
