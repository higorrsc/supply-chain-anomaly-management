import pytest
from pydantic import ValidationError

from src.anomaly.domain.rules import (
    AnomalyRules,
    AnomalyThresholds,
    BusinessHoursRule,
    DeviationRule,
    MaxQuantityRule,
    RulesConfig,
)


def test_anomaly_rules_validation() -> None:
    # Valid
    rules = AnomalyRules(
        enabled=True,
        rules=RulesConfig(
            deviation=DeviationRule(
                thresholds=AnomalyThresholds(low=1.5, high=2.5, critical=3.5)
            ),
            business_hours=BusinessHoursRule(enabled=False),
            max_quantity=MaxQuantityRule(enabled=False),
        ),
    )
    assert rules.rules.deviation.thresholds.low == 1.5

    # Invalid
    with pytest.raises(ValidationError):
        AnomalyRules(  # type: ignore[arg-type]
            rules=RulesConfig(
                deviation=DeviationRule(
                    thresholds=AnomalyThresholds.model_validate({"low": 1.5})
                ),
                business_hours=BusinessHoursRule(enabled=False),
                max_quantity=MaxQuantityRule(enabled=False),
            )
        )
