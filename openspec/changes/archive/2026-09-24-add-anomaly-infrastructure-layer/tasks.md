# Tasks

## 1. Models and Mappers

- [x] 1.1 Create `AnomalyModel` in `src/anomaly/infrastructure/models/anomaly_model.py` inheriting from `Base` and mapping UUID, Decimal, and Enum fields correctly. Verify by ensuring the file passes linting and type checks.
- [x] 1.2 Create `AnomalyMapper` in `src/anomaly/infrastructure/mappers/anomaly_mapper.py` with `to_entity`, `to_model`, and `update_model` methods. Verify by writing unit tests in `tests/anomaly/infrastructure/mappers/test_anomaly_mapper.py`.
- [x] 1.3 Create `AnomalyAlertModel` in `src/anomaly/infrastructure/models/anomaly_alert_model.py` mapping UUIDs and boolean fields. Verify by ensuring it passes linting and type checks.
- [x] 1.4 Create `AnomalyAlertMapper` in `src/anomaly/infrastructure/mappers/anomaly_alert_mapper.py`. Verify by writing unit tests in `tests/anomaly/infrastructure/mappers/test_anomaly_alert_mapper.py`.

## 2. Repositories

- [x] 2.1 Implement `AnomalyRepository` in `src/anomaly/infrastructure/repositories/anomaly_repository.py` inheriting from `SqlAlchemyRepository` and `IAnomalyRepository`. Verify by writing integration tests with SQLite or an async DB test fixture in `tests/anomaly/infrastructure/repositories/test_anomaly_repository.py`.
- [x] 2.2 Implement `AnomalyAlertRepository` in `src/anomaly/infrastructure/repositories/anomaly_alert_repository.py` inheriting from `SqlAlchemyRepository` and `IAnomalyAlertRepository`, implementing `get_by_anomaly_id`. Verify by writing integration tests in `tests/anomaly/infrastructure/repositories/test_anomaly_alert_repository.py`.

## 3. Database Exposing

- [x] 3.1 Expose `AnomalyModel` and `AnomalyAlertModel` in `src/anomaly/infrastructure/models/__init__.py` and ensure they are imported in `migrations/env.py` (if they are not already dynamically discovered, or by updating the base imports). Verify by checking the `env.py` script.
