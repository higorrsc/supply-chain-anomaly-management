# Tasks

## 1. API Schemas

- [x] 1.1 Create `AnomalyResponse` and `AnomalyAlertResponse` Pydantic models in `src/anomaly/presentation/api/schemas/anomaly_schema.py`. Verify by ensuring the file passes linting.
- [x] 1.2 Create `RegisterAnomalyRequest` Pydantic model in `src/anomaly/presentation/api/schemas/anomaly_schema.py`. Verify by ensuring the file passes linting.

## 2. Dependencies and Setup
- [x] 2.0 Add `fastapi` and `uvicorn` to project dependencies (via `uv add`). Verify by checking `pyproject.toml`.

- [x] 2.1 Create a dependencies provider in `src/anomaly/presentation/api/dependencies.py` that provides instances of the `AnomalyRepository` and the various use cases (e.g., `get_register_anomaly_use_case`, `get_anomaly_by_id_use_case`) using FastAPI's `Depends` and the database session. Verify by checking if it type checks.

## 3. Controllers / Routers

- [x] 3.1 Create the FastAPI `APIRouter` in `src/anomaly/presentation/api/controllers/anomaly_controller.py`. Verify by ensuring the router is instantiated correctly.
- [x] 3.2 Implement the `POST /` endpoint to register an anomaly, mapping the Pydantic request to the Application DTO and returning a 201 status code with the created `AnomalyResponse`. Verify by writing a test using `TestClient` or `AsyncClient`.
- [x] 3.3 Implement the `GET /{anomaly_id}` endpoint, handling `AnomalyNotFoundError` by raising an `HTTPException(404)`. Verify by writing a test.
- [x] 3.4 Implement the `PUT /{anomaly_id}/resolve` endpoint to resolve an anomaly. Verify by writing a test.
- [x] 3.5 Implement the `GET /{anomaly_id}/alerts` endpoint to retrieve anomaly alerts. Verify by writing a test.
- [x] 3.6 Implement the `GET /` endpoint to search anomalies (using `SearchCriteria` mapping from query parameters). Verify by writing a test.
