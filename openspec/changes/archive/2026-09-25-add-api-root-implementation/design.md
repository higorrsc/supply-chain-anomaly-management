# Design

## Context

The application logic (Domain and Application layers) and presentation components (FastAPI controllers and dependencies) for `anomaly` and `inventory` bounded contexts are ready. The database is set up and accessible via `docker-compose`. However, we lack the central FastAPI application that ties these routers together, configures middlewares (CORS), and manages the lifecycle (startup/shutdown) to initialize database resources.

## Goals / Non-Goals

**Goals:**

- Create the FastAPI application root in `src/main.py`.
- Configure basic CORS middleware.
- Create an API versioning router (`/api/v1`) and mount the `anomaly` and `inventory` context routers onto it.
- Wire up the database connection pool using FastAPI lifecycle events.

**Non-Goals:**

- Implementing authentication or authorization middlewares (out of scope for this change).
- Comprehensive error handler overrides beyond standard FastAPI behaviors.

## Decisions

- **Entry Point:** The application will be located at `src/main.py` rather than `src/core/presentation/api/main.py` to follow standard FastAPI conventions, making it easier for tools like Uvicorn to discover (`uvicorn src.main:app`).
- **Versioning:** We will use a dedicated APIRouter prefix for versioning (e.g., `/api/v1`). Context routers (`/anomalies`, `/items`, `/warehouses`, `/movements`) will be included in this v1 router.
- **Database Lifecycle:** We will use FastAPI's `@asynccontextmanager` lifespan event to initialize database connections (if required by SQLAlchemy configuration, though typically handled via sessionmakers lazily, we should ensure the DB config module is correctly wired).

## Risks / Trade-offs

- **Risk:** Database connection failures on startup if the database isn't ready.
  - **Mitigation:** Rely on docker-compose `depends_on` and `healthcheck` to ensure the DB is ready before the API server boots.
- **Risk:** CORS configuration is too permissive.
  - **Mitigation:** We'll start with a permissive standard for development (`allow_origins=["*"]`) but configure it through settings so it can be restricted in production.
