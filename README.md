# Supply Chain Anomaly Management

A comprehensive web application designed to manage and monitor supply chain stock movements, detecting anomalies in real-time based on statistical patterns. Built with **Domain-Driven Design (DDD)**, **Clean Architecture**, and **SOLID** principles.

## 🚀 Features

- **Inventory Management:** Create and manage items, warehouses, and track real-time movements.
- **Real-time Anomaly Detection:** Intercepts stock movements and applies statistical rules to flag anomalies based on historical deviation.
- **Interactive Dashboard:** A dark-themed, Streamlit-based UI for visualizing KPIs, filtering anomalies, and tracking supply chain health.
- **Robust API:** A modern FastAPI backend offering structured endpoints for resolving anomalies and registering movements.
- **Asynchronous Architecture:** PostgreSQL integration using SQLAlchemy's async engine for high concurrency.

## 🛠 Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy (async), Pydantic
- **Frontend:** Streamlit, Pandas, Altair
- **Database:** PostgreSQL (with Alembic for migrations)
- **Infrastructure:** Docker, Docker Compose, Nginx
- **Tooling:** uv, Ruff, MyPy, Pytest

## 🚀 Getting Started

1. Clone the repository.
2. Ensure you have Docker and Docker Compose installed.
3. Start the application:

   ```bash
   docker compose up -d
   ```

4. Access the Dashboard at: [http://localhost](http://localhost)
5. Access the API documentation (Swagger) at: [http://localhost/docs](http://localhost/docs)

## ⚙️ Configuring Anomaly Rules (`anomaly_rules.yaml`)

The anomaly detection engine calculates the historical standard deviation of stock movements for an item. If a new movement exceeds the average by a certain multiple of the standard deviation, it is flagged as an anomaly.

You can configure these rules in the `anomaly_rules.yaml` file located in the root of the project:

```yaml
enabled: true
deviation_thresholds:
  low: 1.5
  high: 2.5
  critical: 3.5
```

### Options

- **`enabled`** (`bool`): Globally toggles the anomaly detection engine on or off.
- **`deviation_thresholds`**:
  - **`low`** (`float`): The minimum multiplier of the standard deviation required to trigger a *Low* severity anomaly.
  - **`high`** (`float`): The multiplier required to trigger a *High* severity anomaly.
  - **`critical`** (`float`): The multiplier required to trigger a *Critical* severity anomaly.

## 🏗 Project Structure

The project is heavily modularized to respect architectural boundaries:

- **[`docs/`](docs/README.md)**: Architectural documentation and guidelines.
- **[`migrations/`](migrations/README.md)**: Alembic database migration scripts.
- **[`nginx/`](nginx/README.md)**: Reverse proxy configuration.
- **[`openspec/`](openspec/README.md)**: Specifications and changes managed by OpenSpec.
- **[`scripts/`](scripts/README.md)**: Utility scripts (e.g., database seeders).
- **[`src/`](src/README.md)**: The core application source code.
- **[`tests/`](tests/README.md)**: Automated test suites (Unit, Integration, E2E).
