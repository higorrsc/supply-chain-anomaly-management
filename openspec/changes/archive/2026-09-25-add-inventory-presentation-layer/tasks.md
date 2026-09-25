# Tasks

## 1. Pydantic Schemas

- [x] 1.1 Create `ItemResponse`, `RegisterItemRequest`, and `UpdateItemRequest` schemas in `src/inventory/presentation/api/schemas/item_schema.py`. Ensure Value Object properties (`SKU`) are correctly unwrapped via `@field_validator(mode="before")`. Verify by ensuring the file passes `ruff` and `mypy`.
- [x] 1.2 Create `WarehouseResponse`, `RegisterWarehouseRequest`, and `UpdateWarehouseRequest` schemas in `src/inventory/presentation/api/schemas/warehouse_schema.py`. Verify by ensuring the file passes `ruff` and `mypy`.
- [x] 1.3 Create `MovementResponse`, `RegisterMovementRequest`, and `SearchMovementsResponse` schemas in `src/inventory/presentation/api/schemas/movement_schema.py`. Ensure `Quantity` is unwrapped correctly. Verify by ensuring the file passes `ruff` and `mypy`.
- [x] 1.4 Export all created schemas in `src/inventory/presentation/api/schemas/__init__.py`. Verify by checking the `__all__` list and `ruff check`.

## 2. API Dependencies

- [x] 2.1 Create the API dependency provider in `src/inventory/presentation/api/dependencies.py`. Inject `Depends(get_db_session)` and create provider methods for `ItemRepository`, `WarehouseRepository`, `MovementRepository`, and all `inventory` use cases (e.g. `get_activate_item_use_case`, `get_create_movement_use_case`). Verify by ensuring the file passes `mypy`.
- [x] 2.2 Export the dependency methods in `src/inventory/presentation/api/__init__.py`. Verify by checking the `__all__` list and `ruff check`.

## 3. Controllers

- [x] 3.1 Create `src/inventory/presentation/api/controllers/item_controller.py` providing endpoints for Create, Update, Delete, Activate, Deactivate, Get by ID, Get by SKU, and Search. Handle Domain errors (`EntityNotFoundError`, `ConflictError`, etc.) wrapping them in `HTTPException`. Verify by ensuring the file passes `mypy`.
- [x] 3.2 Create `src/inventory/presentation/api/controllers/warehouse_controller.py` providing endpoints for Create, Update, Delete, Activate, Deactivate, Get by ID, and Search. Verify by ensuring the file passes `mypy`.
- [x] 3.3 Create `src/inventory/presentation/api/controllers/movement_controller.py` providing endpoints for Create, Get by ID, and Search. Verify by ensuring the file passes `mypy`.
- [x] 3.4 Export the routers in `src/inventory/presentation/api/controllers/__init__.py`. Ensure all `from src...` imports throughout the controllers use the exported `__init__.py` module formats. Verify by running `make check`.

## 4. Tests

- [x] 4.1 Write integration tests in `tests/inventory/presentation/api/controllers/test_item_controller.py` mocking the Use Cases and verifying HTTP status codes and responses. Verify by running `pytest`.
- [x] 4.2 Write integration tests in `tests/inventory/presentation/api/controllers/test_warehouse_controller.py`. Verify by running `pytest`.
- [x] 4.3 Write integration tests in `tests/inventory/presentation/api/controllers/test_movement_controller.py`. Verify by running `pytest`.
- [x] 4.4 Run `make check` and verify 100% of formatting, linting, type-checking, and tests pass for the entire project.
