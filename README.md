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

The anomaly detection engine uses a flexible rules system to evaluate stock movements. You can configure multiple types of rules (statistical deviation, business hours, and quantity limits) in the `anomaly_rules.yaml` file located in the root of the project:

```yaml
enabled: true
rules:
  deviation:
    enabled: true
    thresholds:
      low: 1.5
      high: 2.5
      critical: 3.5
  business_hours:
    enabled: true
    start_time: "08:00"
    end_time: "18:00"
  max_quantity:
    enabled: true
    max_in: 100
    max_out: 50
```

### Options

- **`enabled`** (`bool`): Globally toggles the entire anomaly detection engine on or off.
- **`rules.deviation`**: Flags anomalies based on statistical deviation (multiplier of historical average).
  - **`enabled`** (`bool`): Toggles the deviation rule.
  - **`thresholds.low`** / **`high`** / **`critical`** (`float`): The multipliers required to trigger the respective severity levels.
- **`rules.business_hours`**: Flags anomalies for movements occurring outside configured operating hours (UTC).
  - **`enabled`** (`bool`): Toggles the business hours rule.
  - **`start_time`** / **`end_time`** (`str`): The permitted operating hours in `HH:MM` format. Violations trigger a *High* severity anomaly.
- **`rules.max_quantity`**: Flags anomalies for movements that exceed hard-coded quantity limits.
  - **`enabled`** (`bool`): Toggles the maximum quantity rule.
  - **`max_in`** (`int`): Maximum allowed quantity for inbound (`IN`) movements. Violations trigger a *Critical* severity anomaly.
  - **`max_out`** (`int`): Maximum allowed quantity for outbound (`OUT`) movements. Violations trigger a *Critical* severity anomaly.

## 🏗 Project Structure

The project is heavily modularized to respect architectural boundaries:

- **[`docs/`](docs/README.md)**: Architectural documentation and guidelines.
- **[`migrations/`](migrations/README.md)**: Alembic database migration scripts.
- **[`nginx/`](nginx/README.md)**: Reverse proxy configuration.
- **[`openspec/`](openspec/README.md)**: Specifications and changes managed by OpenSpec.
- **[`scripts/`](scripts/README.md)**: Utility scripts (e.g., database seeders).
- **[`src/`](src/README.md)**: The core application source code.
- **[`tests/`](tests/README.md)**: Automated test suites (Unit, Integration, E2E).
