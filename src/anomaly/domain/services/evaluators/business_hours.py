from datetime import datetime

from src.anomaly.domain.enums.anomaly_severity import AnomalySeverity
from src.anomaly.domain.rules import AnomalyRules
from src.anomaly.domain.services.evaluators.base import RuleEvaluator, RuleResult
from src.inventory.domain.events import MovementCreatedEvent


class BusinessHoursEvaluator(RuleEvaluator):
    def evaluate(
        self, event: MovementCreatedEvent, rules: AnomalyRules
    ) -> RuleResult | None:
        business_rules = rules.rules.business_hours
        if not business_rules.enabled:
            return None

        # Parse start and end times (Format: "HH:MM")
        try:
            start_dt = datetime.strptime(business_rules.start_time, "%H:%M").time()
            end_dt = datetime.strptime(business_rules.end_time, "%H:%M").time()
        except ValueError:
            return None

        movement_time = event.occurrence_date.time()

        if not (start_dt <= movement_time <= end_dt):
            # If outside business hours, it's flagged as an anomaly.
            # Using HIGH severity with a fixed score as a rule of thumb.
            return RuleResult(severity=AnomalySeverity.HIGH, score=50.0)

        return None
