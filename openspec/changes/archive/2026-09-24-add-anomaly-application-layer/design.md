# Design

## Context

The `anomaly` domain models are already in place. This design establishes the Application layer, following the CQRS (Command Query Responsibility Segregation) pattern as established in the `inventory` context.

## Goals / Non-Goals

**Goals:**
- Provide clear orchestration Use Cases for anomalies.
- Use Pydantic DTOs for data transfer in and out of the Application layer.
- Integrate strictly with `IAnomalyRepository` and `IAnomalyAlertRepository`.

**Non-Goals:**
- No API controllers (FastAPI) or database mapping (SQLAlchemy) in this phase.
- No direct manipulation of Domain Entities by external layers except through these Use Cases.

## Decisions

**1. CQRS Organization**
- **Decision:** Split the use cases into `commands` (mutating state) and `queries` (reading state).
- **Rationale:** Aligns with Clean Architecture and keeps read vs write dependencies explicit. 

**2. DTO usage**
- **Decision:** Inputs to Use Cases will be passed as kwargs or specific input DTOs. Outputs will be returned as primitive types, domain entities, or specific output DTOs.
- **Rationale:** Ensures we do not leak infrastructure constraints into the application layer.

## Risks / Trade-offs

- **Risk:** Resolving an anomaly requires transactional integrity.
  **Mitigation:** The application layer must rely on Unit of Work (if available in the core structure) or rely on repository `.save()` methods safely.
