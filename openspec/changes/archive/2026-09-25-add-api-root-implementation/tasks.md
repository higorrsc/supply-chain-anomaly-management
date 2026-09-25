# Tasks

## 1. Application Root Configuration

- [x] 1.1 Create `src/core/presentation/api/main.py`. Note: According to the design, we will place the file at `src/main.py`. Wait, let's stick to `src/main.py` directly. So, create `src/main.py` containing the `FastAPI()` app initialization. Configure basic CORS middleware. Verify by ensuring the file passes `ruff` and `mypy`.
- [x] 1.2 In `src/main.py`, define the application lifespan `@asynccontextmanager` to handle startup events if the database engine needs it, or simply rely on standard SQLAlchemy async engine initialization from `src/core/infrastructure/database/session.py`. Verify by running `make check`.

## 2. Router Integration

- [x] 2.1 Create an API versioning router `api_v1_router = APIRouter(prefix="/api/v1")` inside `src/main.py` (or extracted into a router module if necessary, but `main.py` is fine for now). Verify by checking the file syntax.
- [x] 2.2 Import the Anomaly controller router (`from src.anomaly.presentation.api.controllers import router as anomaly_router`) and include it in `api_v1_router`. Verify by ensuring the file passes `mypy`.
- [x] 2.3 Import the Inventory controller routers (`item_router`, `warehouse_router`, `movement_router`) from `src.inventory.presentation.api.controllers` and include them in `api_v1_router`. Verify by ensuring the file passes `mypy`.
- [x] 2.4 Include `api_v1_router` in the root `FastAPI()` app. Verify by ensuring `make check` passes.

## 3. Integration Testing

- [x] 3.1 Create a simple health check or root endpoint (`/` or `/health`) in `src/main.py` to confirm the API is up. Verify by ensuring the file passes `ruff` and `mypy`.
- [x] 3.2 Write a test `tests/test_main.py` using `TestClient` to verify the `/health` endpoint returns `200 OK`. Verify by running `pytest`.
