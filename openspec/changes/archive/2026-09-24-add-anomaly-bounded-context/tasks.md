# Tasks

## 1. Domain Types and Value Objects

- [x] 1.1 Create `AnomalyStatus` and `AnomalySeverity` enums in `src/anomaly/domain/enums` and verify with basic instantiations in a unit test.
- [x] 1.2 Create the `Score` value object in `src/anomaly/domain/value_objects`, ensuring min/max validation is implemented and unit tested.
- [x] 1.3 Add custom exceptions (`InvalidAnomalyError`, `InvalidScoreError`) in `src/anomaly/domain/exceptions.py` and verify they can be raised.

## 2. Domain Entities

- [x] 2.1 Create the `Anomaly` entity in `src/anomaly/domain/entities/anomaly.py` utilizing the new enums and value object, and verify it passes unit tests for creation and status transitions.
- [x] 2.2 Create the `AnomalyAlert` entity in `src/anomaly/domain/entities/anomaly_alert.py` with necessary associations to the anomaly, and verify it with unit tests.

## 3. Domain Repositories

- [x] 3.1 Define the interface `IAnomalyRepository` in `src/anomaly/domain/repositories/i_anomaly.py` and verify it correctly inherits from `AbstractRepository`.
- [x] 3.2 Define the interface `IAnomalyAlertRepository` in `src/anomaly/domain/repositories/i_anomaly_alert.py` and verify it correctly inherits from `AbstractRepository`.
- [x] 3.3 Ensure the `src/anomaly/domain` layer correctly exports all elements in `__init__.py` files and runs cleanly through MyPy and Ruff.
