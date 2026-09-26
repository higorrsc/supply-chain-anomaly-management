from decimal import Decimal

from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.rules import AnomalyRules
from src.anomaly.domain.services.evaluators.base import RuleEvaluator, RuleResult
from src.inventory.domain.events import MovementCreatedEvent


class MaxQuantityEvaluator(RuleEvaluator):
    def evaluate(
        self, event: MovementCreatedEvent, rules: AnomalyRules
    ) -> RuleResult | None:
        max_qty_rule = rules.rules.max_quantity
        if not max_qty_rule.enabled:
            return None

        qty = Decimal(str(event.quantity_value))

        if event.movement_type.name == "IN" and qty > max_qty_rule.max_in:
            # Flag as CRITICAL if it breaches max quantity
            return RuleResult(severity=AnomalySeverity.CRITICAL, score=100.0)
        elif event.movement_type.name == "OUT" and qty > max_qty_rule.max_out:
            return RuleResult(severity=AnomalySeverity.CRITICAL, score=100.0)

        return None
