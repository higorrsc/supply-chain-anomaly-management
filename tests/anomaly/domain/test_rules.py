from pydantic import ValidationError
import pytest
from src.anomaly.domain.rules import AnomalyRules

def test_anomaly_rules_validation():
    # Valid
    rules = AnomalyRules(
        enabled=True,
        deviation_thresholds={"low": 1.5, "high": 2.5, "critical": 3.5}
    )
    assert rules.deviation_thresholds.low == 1.5
    
    # Invalid
    with pytest.raises(ValidationError):
        AnomalyRules(deviation_thresholds={"low": 1.5})
