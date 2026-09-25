# Proposal

## Why

The controllers for both Anomaly and Inventory contexts are complete, but they are not currently hooked up to a runnable API server. We need to implement the root FastAPI application to expose these endpoints, provide API versioning support (e.g., `/api/v1`), configure CORS, and integrate it with the existing PostgreSQL database spun up via `docker-compose`.

## What Changes

- Create the root FastAPI application instance.
- Configure CORS middleware.
- Create an API router (v1) and register both Anomaly and Inventory routers under it.
- Ensure the application properly connects to the PostgreSQL database by defining its lifespan events (startup/shutdown) or verifying the SQLAlchemy async engine configurations.
- Update `main.py` to run the application using `uvicorn`.
- Provide a `docker-compose` override or entrypoint instruction if necessary, but the primary task is to connect the Python code to the existing DB.

## Capabilities

### New Capabilities

None. This is an architectural and infrastructure plumbing change. `skip_specs` is set to true.

### Modified Capabilities

None.

## Impact

- `src/main.py` and potentially `src/core/presentation/` files will be added or modified.
- The system will become runnable and accessible via HTTP.
- Dependencies such as `fastapi[standard]` and `uvicorn[standard]` are already installed.
