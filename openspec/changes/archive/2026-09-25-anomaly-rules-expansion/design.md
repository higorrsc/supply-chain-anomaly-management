# Design

## Context

The application currently relies entirely on statistical deviation to flag anomalies. The engine is tightly coupled to this single heuristic in `AnomalyDetectionService`. We need to introduce a generic Rule Engine approach where different evaluators (Deviation, Business Hours, Max Quantity) can independently analyze a movement and contribute to an aggregated anomaly result.

## Goals / Non-Goals

**Goals:**

- Implement a flexible rule-evaluation system inside the anomaly engine.
- Update Pydantic configuration schemas (`AnomalyConfig` in `src/anomaly/infrastructure/config/settings.py`) to parse new complex nested rule structures.
- Accumulate multiple anomaly reasons if a movement breaches more than one rule (e.g., "Outside business hours" AND "Critical Quantity").

**Non-Goals:**

- We are not creating a dynamic UI builder for rules; they will remain statically configured via `anomaly_rules.yaml`.
- We are not persisting rule history. The anomalies will just store the severity and score at the time of detection.

## Decisions

**1. Rule Evaluation Pattern:**
We will refactor `AnomalyDetectionService` to iterate through a registry of rule evaluators. Each evaluator implements a common interface (e.g., `def evaluate(movement, context) -> RuleResult`).

- *Alternative considered:* Hardcoding the `if` checks in the service. *Rejected* because it violates the Open/Closed Principle.

**2. Configuration Schema:**
We will introduce new Pydantic models for the rules:

```python
class BusinessHoursRule(BaseModel):
    enabled: bool = False
    start_time: str = "08:00"
    end_time: str = "18:00"


class MaxQuantityRule(BaseModel):
    enabled: bool = False
    max_in: int = 100
    max_out: int = 50
```

This allows strong validation at application startup.

**3. Aggregating Scores:**
If a movement violates the business hours rule, it gets a flat score (e.g., 50 - HIGH). If it violates the deviation rule, it gets its calculated score. The final anomaly entity will store the *highest* severity encountered, and the reason field (if we decide to add one) or we just leave the entity as is and use a generic highest severity. Since `Anomaly` entity doesn't currently have a `reason` text column, we will just take the highest severity and maximum score to avoid complex database migrations right now.

## Risks / Trade-offs

- **Risk:** Timezone handling for business hours. `datetime.now(UTC)` vs local warehouse time.
  - *Mitigation:* The `business_hours` rule will assume UTC for now unless timezone logic is strictly enforced. We will document that the config hours should be in UTC.
