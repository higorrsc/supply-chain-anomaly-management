from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.rules import AnomalyRules
from src.anomaly.domain.services.evaluators.base import RuleEvaluator, RuleResult
from src.inventory.domain.events import MovementCreatedEvent


class DeviationEvaluator(RuleEvaluator):
    def evaluate(
        self, event: MovementCreatedEvent, rules: AnomalyRules
    ) -> RuleResult | None:
        deviation_rule = rules.rules.deviation
        if not deviation_rule.enabled:
            return None

        qty = float(event.quantity_value)
        score_value = round(qty / 100.0, 4)

        if score_value >= deviation_rule.thresholds.critical:
            return RuleResult(severity=AnomalySeverity.CRITICAL, score=score_value)
        elif score_value >= deviation_rule.thresholds.high:
            return RuleResult(severity=AnomalySeverity.HIGH, score=score_value)
        elif score_value >= deviation_rule.thresholds.low:
            return RuleResult(severity=AnomalySeverity.LOW, score=score_value)

        return None
