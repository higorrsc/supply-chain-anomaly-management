# Proposal

## Why

The `inventory` bounded context currently lacks a presentation layer (API endpoints, controllers, schemas, and dependencies). To expose its use cases to the outside world and allow interactions via HTTP (following the same structure implemented in the `anomaly` context), we need to build its presentation layer using FastAPI and Pydantic schemas.

## What Changes

- Create Pydantic schemas for `Item`, `Warehouse`, and `Movement` requests and responses in `src/inventory/presentation/api/schemas/`.
- Create a FastAPI dependency provider in `src/inventory/presentation/api/dependencies.py` to inject Repositories and Use Cases.
- Create FastAPI controllers (`item_controller.py`, `warehouse_controller.py`, `movement_controller.py`) in `src/inventory/presentation/api/controllers/`.
- Properly define and populate `__init__.py` files across the `inventory/presentation` module to ensure clean and correct imports (e.g. `from src.inventory.presentation.api.schemas import ItemResponse`).
- Write Pytest integration tests for all implemented controllers in `tests/inventory/presentation/api/controllers/`.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
None.

*(Note: We have set `skip_specs: true` in `.openspec.yaml` since this is purely a structural plumbing/API layer implementation for existing use cases, and no functional requirements are changing).*

## Impact

- **API:** New endpoints under `/items`, `/warehouses`, and `/movements`.
- **Architecture:** Connects existing Application layer use cases to the HTTP Presentation boundary.
- **Dependencies:** Uses FastAPI routing and dependency injection.
