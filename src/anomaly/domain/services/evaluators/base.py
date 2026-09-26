from typing import Protocol

from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.rules import AnomalyRules
from src.inventory.domain.events import MovementCreatedEvent


class RuleResult:
    def __init__(self, severity: AnomalySeverity, score: float):
        self.severity = severity
        self.score = score


class RuleEvaluator(Protocol):
    def evaluate(
        self, event: MovementCreatedEvent, rules: AnomalyRules
    ) -> RuleResult | None: ...
