# Application Source Code (`src/`)

This directory contains the entire application codebase, organized around Bounded Contexts and Clean Architecture principles.

## Modules

- **[`core/`](core/README.md)**: Shared interfaces, base abstractions, and common infrastructure (e.g., base repositories, Unit of Work, pagination).
- **[`inventory/`](inventory/README.md)**: The Inventory bounded context. Manages Items, Warehouses, and stock Movements.
- **[`anomaly/`](anomaly/README.md)**: The Anomaly bounded context. Contains the rules and engine for detecting and resolving supply chain anomalies.
- **[`dashboard/`](dashboard/README.md)**: The Streamlit presentation layer. Consumes the backend APIs to provide a visual interface.
- **`main.py`**: The FastAPI application entrypoint, responsible for wiring dependencies and mounting routers.
