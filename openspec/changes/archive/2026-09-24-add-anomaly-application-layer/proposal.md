# Proposal

## Why

The domain models for the `anomaly` bounded context have been successfully implemented. To make this domain functional and accessible to outer layers (like presentation/API), we need an Application layer consisting of Use Cases and Data Transfer Objects (DTOs) that orchestrate the domain rules.

## What Changes

- Create DTOs (Data Transfer Objects) using Pydantic for input validation.
- Implement Commands (Use Cases) for: `RegisterAnomaly`, `ResolveAnomaly`, `GenerateAnomalyAlert`.
- Implement Queries (Use Cases) for: `GetAnomalyById`, `SearchAnomaly`, `GetAlertsByAnomalyId`.
- Setup application exceptions (e.g. `AnomalyNotFoundError`).
- Introduce Unit of Work or Ports where necessary to handle database transactions cleanly.

## Capabilities

### New Capabilities

- 

### Modified Capabilities

- 

## Impact

- Adds the `src/anomaly/application` layer, containing `dto`, `use_cases/commands`, and `use_cases/queries`.
- Sets up the core application boundaries necessary to expose the `anomaly` features to HTTP/FastAPI routes later.
