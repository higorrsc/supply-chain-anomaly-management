# Design

## Context

We are implementing the FastAPI presentation layer for the `inventory` bounded context, which encompasses `Item`, `Warehouse`, and `Movement` domain concepts. See proposal.md for motivation - this aligns the `inventory` presentation layer with the recently built `anomaly` presentation layer.

## Goals / Non-Goals

**Goals:**
- Provide complete RESTful routing for existing `inventory` Use Cases.
- Create Pydantic input and output schemas mirroring domain objects, properly mapped from/to DTOs.
- Maintain dependency injection parity with the `anomaly` context.
- Ensure correct and concise `__init__.py` behavior (explicitly required by the user).

**Non-Goals:**
- Modifying existing Domain or Application Use Case rules.
- Writing any frontend code or consuming clients.
- Implementing features not already present in the Application layer.

## Decisions

- **Routing Separation**: We will use a separate `APIRouter` for each entity (e.g., `item_controller.py`, `warehouse_controller.py`, `movement_controller.py`) to prevent a bloated controller file.
- **Pydantic Model Definitions**: Each entity will have its own schema file (`item_schema.py`, `warehouse_schema.py`, `movement_schema.py`). We will use `field_validator` with `mode="before"` to unpack Value Objects like `SKU` or `Quantity` during the `from_attributes=True` validation of domain models.
- **Dependency Wiring**: `dependencies.py` will contain `Depends(get_db_session)` and construct the respective Repositories and Use Cases for all three domains within the `inventory` context.
- **`__init__.py` Strict Use**: We will populate all `__init__.py` files as requested and use paths like `from src.inventory.presentation.api.schemas import ItemResponse` inside our controllers. Repetitive external imports (like `Settings` from `core`) will be mapped through their respective `__init__.py` files if they are not already, ensuring proper modular exports are used.

## Risks / Trade-offs

- **Risk**: Value Objects (like `SKU`, `Quantity`) from domain entities might crash Pydantic serialization if they are not properly coerced to primitives (strings/decimals).
  - **Mitigation**: We will use Pydantic `@field_validator(mode="before")` on schema fields pointing to these value objects to call `getattr(v, "value", v)` before Pydantic validates the base primitive type, exactly like we did with `Score` in the `anomaly` context.

## Open Questions
None.
