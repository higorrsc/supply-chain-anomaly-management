# Automated Tests (`tests/`)

This directory contains the automated test suite, enforcing quality and correctness.

## Structure
- **`core/`, `inventory/`, `anomaly/`**: Tests are grouped by bounded context.
- **`fakes/`**: In-memory implementations of repositories and services to enable fast, database-free unit testing of application use-cases.
- **`e2e/`**: End-to-end tests validating the complete flow from HTTP request to database persistence.

## Running Tests
Run the entire suite using:
```bash
uv run pytest
```
