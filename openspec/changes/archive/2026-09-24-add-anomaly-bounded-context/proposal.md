# Proposal

## Why

The supply chain anomaly management system requires a dedicated bounded context to process stock movements, detect deviations using historical data, and classify anomalies. Introducing the `anomaly` bounded context separates these analytical and detection concerns from core inventory management, adhering to DDD and Clean Architecture principles.

## What Changes

- Create the `anomaly` bounded context mirroring the architectural structure of the `inventory` context.
- Introduce Domain Entities: `Anomaly` and `AnomalyAlert`.
- Introduce Value Objects: `Score` (to represent deviation or severity score).
- Introduce Enums: `AnomalyStatus` and `AnomalySeverity`.
- Introduce Domain Exceptions for anomaly validation.
- Setup domain repositories interfaces: `IAnomalyRepository` and `IAnomalyAlertRepository`.

## Capabilities

### New Capabilities

- `anomaly-management`: Covers the detection, classification, and management of anomalies within the supply chain, including calculating anomaly scores and generating alerts based on severity and status.

### Modified Capabilities

-

## Impact

- **New Code**: Adds a complete domain layer inside `src/anomaly/domain/`.
- **System Boundaries**: Establishes the separation between inventory tracking (which provides historical data) and anomaly detection (which evaluates it).
