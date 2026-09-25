# Proposal

## Why

Currently, anomaly detection thresholds are hardcoded, and the analysis process is not fully integrated with the stock movement event stream. We need a system that automatically analyzes stock movements upon creation using configurable rules (via a YAML file). This allows business analysts to adjust detection parameters without requiring code changes, and provides the foundation for Streamlit dashboards to visualize these anomalies in real-time.

## What Changes

- Implement an event-driven mechanism (e.g., domain events) to trigger anomaly analysis automatically whenever a new stock movement is registered.
- Introduce a YAML configuration file to define anomaly detection rules (e.g., standard deviation thresholds, moving average windows, allowed deviation percentages).
- Create a domain service/configuration parser to load and apply these YAML rules during the anomaly detection process.
- Modify existing anomaly creation logic to evaluate the movement against the loaded configuration instead of hardcoded rules.

## Capabilities

### New Capabilities

- `movement-analysis-rules`: Specifies the YAML configuration structure and how its rules are loaded and applied to stock movements.

### Modified Capabilities

- `anomaly-management`: Updates the requirement for anomaly registration to specify that it is triggered automatically by stock movement events and evaluated using dynamically loaded configuration rules.

## Impact

- **Event System**: Introduces or expands the domain event system to connect the Inventory bounded context (movement creation) with the Anomaly bounded context (analysis).
- **Configuration**: Adds a new configuration dependency (YAML file) for the application environment.
- **Domain Services**: Refactors the anomaly detection logic to depend on the dynamic rules configuration.
