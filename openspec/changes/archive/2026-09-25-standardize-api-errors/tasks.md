# Tasks

## 1. RFC 7807 Pydantic Schema

- [x] 1.1 Create `RFC7807Error` Pydantic model in a shared location (e.g., `src/core/presentation/api/schemas.py`) containing fields `type`, `title`, `status`, `detail`, `instance`. Verify with `uv run mypy .`.

## 2. Update Global Exception Handlers

- [x] 2.1 Refactor `domain_error_handler` in `src/main.py` to return the `RFC7807Error` schema (HTTP 400). Use `request.url.path` for `instance`. Verify by running the API and checking the response structure.
- [x] 2.2 Refactor `entity_not_found_handler` in `src/main.py` to return the `RFC7807Error` schema (HTTP 404). Verify by running the API and checking the response structure.
- [x] 2.3 Refactor `entity_validation_error_handler` in `src/main.py` to return the `RFC7807Error` schema (HTTP 422). Verify by running the API and checking the response structure.
- [x] 2.4 Refactor `conflict_error_handler` in `src/main.py` to return the `RFC7807Error` schema (HTTP 409). Verify by running the API and checking the response structure.
- [x] 2.5 Ensure the API responses specify the standard MIME type `application/problem+json` for error responses. Verify by making an error request using curl or Swagger.

## 3. Testing and Validation

- [x] 3.1 Run unit tests and make sure no tests are broken by the changed error format. Verify with `make check`.
- [x] 3.2 Add specific integration tests for error format validation (Optional but recommended). Verify with `uv run pytest`.
