# Design

## Context

We are introducing a new bounded context (`src/anomaly`) to handle supply chain anomalies. The architectural pattern must mirror the existing `src/inventory` context, adhering strictly to Domain-Driven Design (DDD), Clean Architecture, and SOLID principles as dictated by `AGENTS.md`.

## Goals / Non-Goals

**Goals:**

- Design a modular bounded context for anomalies.
- Implement isolated Domain Entities, Value Objects, and Enums without leaking infrastructure details.
- Provide strong typing and validation within the domain models.

**Non-Goals:**

- Do not implement presentation or API layers in this phase.
- Do not implement database (SQLAlchemy) persistence models in this phase (focus on the domain layer).
- Do not couple the `anomaly` domain with the `inventory` domain directly; they should interact via Application layer use cases or events.

## Decisions

**1. Domain Entities and Aggregates**

- **Decision:** Create `Anomaly` as the aggregate root and `AnomalyAlert` as a separate entity (or part of the anomaly aggregate depending on lifecycle).
- **Rationale:** Separating the anomaly record from the alert allows us to maintain anomalies without always triggering alerts (e.g., LOW severity).

**2. Value Objects and Enums**

- **Decision:** Use an Enum for `AnomalyStatus` (`OPEN`, `RESOLVED`) and `AnomalySeverity` (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`). Use a Value Object `Score` for the deviation score.
- **Rationale:** Value Objects encapsulate validation (e.g., ensuring a score is a valid decimal/float within expected bounds). Enums enforce a finite set of statuses and severities without relying on raw strings.

**3. Framework-Independent Domain**

- **Decision:** The `src/anomaly/domain` layer will depend only on Python standard libraries and the base `src.core.domain` structures (e.g., `AbstractEntity`, `AbstractRepository`). No SQLAlchemy, Pydantic, or FastAPI dependencies will exist in the domain layer.
- **Rationale:** Required by Clean Architecture rules defined in the project.

## Risks / Trade-offs

- **Risk:** Duplication of base domain logic (e.g., exception handling formats) between `inventory` and `anomaly`.
  **Mitigation:** Rely on `src/core/domain` abstractions where possible.
- **Risk:** Coupling between `inventory` items and `anomaly` records.
  **Mitigation:** `Anomaly` should store identifiers (e.g., UUIDs) of inventory items or movements rather than direct object references, keeping bounded contexts decoupled.
