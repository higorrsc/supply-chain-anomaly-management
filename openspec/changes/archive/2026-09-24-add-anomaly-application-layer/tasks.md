# Tasks

## 1. DTOs and Application Exceptions

- [x] 1.1 Create generic Application Exceptions for the `anomaly` context in `src/anomaly/application/exceptions.py` (e.g., `AnomalyNotFoundError`, `AnomalyAlertNotFoundError`) and verify they can be raised.
- [x] 1.2 Create input/output DTOs for anomalies in `src/anomaly/application/dto/anomaly_dto.py` (e.g., `RegisterAnomalyInput`, `AnomalyOutput`) using Pydantic, and verify with unit tests.
- [x] 1.3 Create input/output DTOs for anomaly alerts in `src/anomaly/application/dto/anomaly_alert_dto.py` and verify with unit tests.

## 2. Command Use Cases

- [x] 2.1 Implement `RegisterAnomalyUseCase` in `src/anomaly/application/use_cases/commands/register_anomaly.py`, ensuring it handles domain logic correctly, saves via repository, and passes unit tests.
- [x] 2.2 Implement `ResolveAnomalyUseCase` in `src/anomaly/application/use_cases/commands/resolve_anomaly.py`, ensuring it transitions status to resolved and passes unit tests.
- [x] 2.3 Implement `GenerateAnomalyAlertUseCase` in `src/anomaly/application/use_cases/commands/generate_anomaly_alert.py`, automatically executing for HIGH/CRITICAL severities, and verify with unit tests.

## 3. Query Use Cases

- [x] 3.1 Implement `GetAnomalyByIdUseCase` in `src/anomaly/application/use_cases/queries/get_anomaly_by_id.py` and verify with unit tests.
- [x] 3.2 Implement `SearchAnomalyUseCase` (e.g. paginated search or simple list) in `src/anomaly/application/use_cases/queries/search_anomaly.py` and verify with unit tests.
- [x] 3.3 Implement `GetAlertsByAnomalyIdUseCase` in `src/anomaly/application/use_cases/queries/get_alerts_by_anomaly_id.py` and verify with unit tests.
