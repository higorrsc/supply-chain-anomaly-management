# Anomaly Module (`src/anomaly/`)

The Anomaly bounded context is responsible for safeguarding the supply chain by identifying suspicious or abnormal stock movements.

## Domain Concepts

- **Anomaly**: An entity representing a flagged movement. Tracks severity, score, and resolution status.
- **Anomaly Detection Service**: A domain service that implements the statistical rules based on standard deviations (configured via `anomaly_rules.yaml`).
