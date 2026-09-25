# Design

## Context

See proposal.md for motivation. We are introducing dynamic configurable rules to detect stock anomalies automatically when a movement occurs, shifting away from hardcoded anomaly rules.

## Goals / Non-Goals

**Goals:**
- Provide a robust way to load and validate YAML configurations for anomaly detection rules using Pydantic.
- Integrate anomaly detection into the movement lifecycle without creating tight coupling between the `Inventory` and `Anomaly` bounded contexts.
- Define a domain service or use case that applies the loaded configuration rules to stock movements to determine standard deviations or threshold breaches.

**Non-Goals:**
- Building the Streamlit dashboard in this specific task (this task only enables the backend data flow).
- Implementing a full-blown distributed event broker (like Kafka/RabbitMQ) - a simple in-memory or application-level event bus/dispatcher is sufficient for now.

## Decisions

1. **Configuration Loading via Pydantic & PyYAML**: 
   - *Decision*: We will define a Pydantic schema for `AnomalyRules` and use `PyYAML` to load the file, validating it through Pydantic.
   - *Rationale*: Guarantees strongly typed, validated rules throughout the domain logic.
   - *Alternatives*: Custom YAML parsing or loading it as raw dictionaries. Rejected because it lacks schema validation.

2. **Event Dispatching for Decoupling**:
   - *Decision*: Introduce a simple `DomainEventDispatcher` abstraction. `CreateMovementUseCase` will publish a `MovementCreatedEvent`. The anomaly context will subscribe a handler (e.g., `DetectAnomalyForMovementUseCase`) to this event.
   - *Rationale*: Follows Clean Architecture by keeping bounded contexts (Inventory and Anomaly) decoupled.
   - *Alternatives*: Directly injecting `DetectAnomalyUseCase` into `CreateMovementUseCase`. Rejected because it creates cross-context coupling.

3. **Dynamic Rule Domain Service**:
   - *Decision*: Introduce a `MovementAnomalyAnalysisService` domain service in the Anomaly context. This service takes the `AnomalyRules` and calculates the anomaly score for a given movement.
   - *Rationale*: Encapsulates the statistical calculation logic as a business rule, compliant with AGENTS.md guidelines.

## Risks / Trade-offs

- **Risk**: Eventual consistency if the event dispatcher runs asynchronously, meaning a movement might be created but the anomaly could appear a few milliseconds/seconds later.
  **Mitigation**: This is acceptable for anomaly detection and aligns well with the future dashboard consumption which polls or streams data.
- **Risk**: Missing YAML configuration file in production.
  **Mitigation**: Fall back to default internal configurations or fail fast during application startup to prevent silent failures.
