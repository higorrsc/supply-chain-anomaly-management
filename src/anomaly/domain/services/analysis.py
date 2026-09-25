from decimal import Decimal

from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.rules import AnomalyRules
from src.anomaly.domain.value_objects.score import Score
from src.inventory.domain.events import MovementCreatedEvent


class MovementAnomalyAnalysisService:
    def __init__(self, rules: AnomalyRules) -> None:
        self.rules = rules

    def analyze(
        self, event: MovementCreatedEvent
    ) -> tuple[AnomalySeverity | None, Score | None]:
        if not self.rules.enabled:
            return None, None

        # Simplified statistical logic for now using the payload
        qty = float(event.quantity_value)

        # In a real scenario, this would consult historical statistics.
        # Here we just mock a simple check.
        # Suppose a quantity > 100 is high, > 500 is critical

        score_value = Decimal(str(round(qty / 100.0, 4)))

        if score_value >= Decimal(str(self.rules.deviation_thresholds.critical)):
            return AnomalySeverity.CRITICAL, Score(value=score_value)
        elif score_value >= Decimal(str(self.rules.deviation_thresholds.high)):
            return AnomalySeverity.HIGH, Score(value=score_value)
        elif score_value >= Decimal(str(self.rules.deviation_thresholds.low)):
            return AnomalySeverity.LOW, Score(value=score_value)

        return None, None
