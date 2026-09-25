# Tasks

## 1. Core and Generic Repository

- [x] 1.1 Update `SqlAlchemyRepository.search` in `src/core/infrastructure/repositories/sqlalchemy_repository.py` to inspect column types using SQLAlchemy `String`. When the column is `String` and the value is `str`, apply `ilike(f"%{value}%")`. Otherwise, fallback to `==`. Verify via repository unit tests or API calls.

## 2. API Controllers

- [x] 2.1 Update `search_items` in `src/inventory/presentation/api/controllers/item_controller.py` to accept an optional `description: str | None` parameter in the GET endpoint, in addition to the SKU. Pass it down to the filters dictionary. Verify via API call with the description parameter.
- [x] 2.2 Check other listing controllers (such as Warehouse or Movements) and ensure they also receive and pass text filters for searching, like the `name` and `location_code` fields in `Warehouse`. Verify via API calls.

## 3. Quality and Testing

- [x] 3.1 Run the full test suite (unit and integration) via `make check` to ensure the use of `ilike` did not break any existing exact searches.
