# Core Module (`src/core/`)

The Core module provides the foundational building blocks shared across all other bounded contexts.

## Responsibilities

- **Domain**: Abstract entities, base value objects, and generic repository interfaces (`AbstractRepository`, `UnitOfWork`).
- **Application**: Generic base use-cases for standard CRUD operations.
- **Infrastructure**: The SQLAlchemy `Base` model, session management, settings configuration, and the Event Dispatcher.
