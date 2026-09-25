# Design

## Context

See `proposal.md` for motivation. The domain, application (use cases), and infrastructure (repositories) layers are already complete. We now need to expose these use cases via a RESTful HTTP API using FastAPI.

## Goals / Non-Goals

**Goals:**
- Implement FastAPI routes for Anomaly management.
- Map HTTP requests to Application DTOs (`@dataclass`es used in `application/use_cases/commands`).
- Validate incoming HTTP requests using Pydantic schemas at the boundary.
- Handle application exceptions (e.g., `AnomalyNotFoundError`) and translate them to proper HTTP status codes.

**Non-Goals:**
- Implementing the main FastAPI `app` or server configuration if it doesn't already exist (we will just create the `APIRouter` for `anomalies`).
- Adding authentication/authorization (unless already provided by the core infrastructure).

## Decisions

- **Decision:** Use FastAPI `APIRouter` for the `anomaly` context.
  - **Rationale:** Keeps the endpoints isolated and modular, allowing the main application to just `include_router()`.
- **Decision:** Pydantic models for API boundary, not application DTOs.
  - **Rationale:** The application layer uses pure Python dataclasses for its DTOs to remain framework-independent. The presentation layer will use Pydantic `BaseModel` for request/response serialization and validation (e.g. `RegisterAnomalyRequest`), and then map to the application dataclass before invoking the use case.
- **Decision:** Use FastAPI's Dependency Injection (`Depends()`) for Use Cases.
  - **Rationale:** Allows us to inject the database session and instantiate the Repositories and Use Cases cleanly on a per-request basis.

## Risks / Trade-offs

- **Risk:** Type conversion between Pydantic strings (for Enums/UUIDs) and the application DTOs.
  - **Mitigation:** Rely on Pydantic's strict typing to ensure the input data is correctly cast to UUIDs and Enums before passing them to the use case.
