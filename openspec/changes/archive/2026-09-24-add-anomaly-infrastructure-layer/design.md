# Design

## Context

See `proposal.md` for the motivation of this change. The `anomaly` context's domain and application layers are already implemented. We now need to persist anomalies and anomaly alerts to the database using SQLAlchemy, similar to the existing `inventory` implementation.

## Goals / Non-Goals

**Goals:**

- Implement persistence for `Anomaly` and `AnomalyAlert` entities.
- Ensure the implementation follows the repository pattern and uses Data Mappers to isolate the domain from the persistence layer.
- Integrate the ORM models with Alembic for future migrations.

**Non-Goals:**

- Generating or applying the Alembic migrations in this task (migrations should typically be run separately).
- Changes to domain entities or application commands.

## Decisions

- **Decision:** Use Data Mapper pattern with `AnomalyMapper` and `AnomalyAlertMapper`.
  - **Rationale:** Keeps the domain entities (`Anomaly`, `AnomalyAlert`) completely framework-agnostic. The mappers handle the translation between SQLAlchemy `AnomalyModel` (and `AnomalyAlertModel`) and the pure Python domain entities. This is the established pattern in this codebase.
- **Decision:** Models will inherit from `src.core.infrastructure.database.Base`.
  - **Rationale:** Centralizes common definitions (e.g., UUID primary keys, `created_at`, `updated_at` tracking).

## Risks / Trade-offs

- **Risk:** Type translation between Value Objects/Enums and database columns.
  - **Mitigation:** The mappers will explicitly convert `Score` Value Objects to `DECIMAL` (or `Float`/`Numeric`) and `AnomalySeverity`/`AnomalyStatus` Enums to string/varchar representations to match standard DB types.
