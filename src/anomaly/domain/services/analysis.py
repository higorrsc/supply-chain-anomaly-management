from decimal import Decimal

from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.rules import AnomalyRules
from src.anomaly.domain.services.evaluators.business_hours import BusinessHoursEvaluator
from src.anomaly.domain.services.evaluators.deviation import DeviationEvaluator
from src.anomaly.domain.services.evaluators.max_quantity import MaxQuantityEvaluator
from src.anomaly.domain.value_objects.score import Score
from src.inventory.domain.events import MovementCreatedEvent


class MovementAnomalyAnalysisService:
    def __init__(self, rules: AnomalyRules) -> None:
        self.rules = rules
        self.evaluators = [
            BusinessHoursEvaluator(),
            MaxQuantityEvaluator(),
            DeviationEvaluator(),
        ]

    def analyze(
        self, event: MovementCreatedEvent
    ) -> tuple[AnomalySeverity | None, Score | None]:
        if not self.rules.enabled:
            return None, None

        highest_severity: AnomalySeverity | None = None
        highest_score: float = 0.0

        for evaluator in self.evaluators:
            result = evaluator.evaluate(event, self.rules)
            if result:
                if result.score > highest_score:
                    highest_score = result.score

                # Compare severity (CRITICAL > HIGH > LOW)
                severity_ranks = {
                    AnomalySeverity.LOW: 1,
                    AnomalySeverity.HIGH: 2,
                    AnomalySeverity.CRITICAL: 3,
                }

                current_rank = (
                    severity_ranks.get(highest_severity, 0) if highest_severity else 0
                )
                new_rank = severity_ranks.get(result.severity, 0)

                if new_rank > current_rank:
                    highest_severity = result.severity

        if highest_severity:
            return highest_severity, Score(value=Decimal(str(highest_score)))

        return None, None
