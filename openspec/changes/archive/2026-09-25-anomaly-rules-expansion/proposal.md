# Proposal

## Why

Currently, the supply chain anomaly detection system only identifies anomalies based on historical statistical deviations (standard deviation multipliers). To provide better business control and security, we need to expand the rule engine to flag other types of suspicious activities: stock movements occurring outside of configurable business hours, and movements where the quantity exceeds predefined operational limits for both inbound and outbound operations. Furthermore, the system needs to support individually enabling or disabling these specific rules.

## What Changes

- Add a `business_hours` rule to detect movements registered outside of a configurable time window (e.g., 08:00 to 18:00).
- Add a `max_quantity` rule to detect single movements with abnormally large quantities, with separate limits for `IN` and `OUT` operations.
- Update the `anomaly_rules.yaml` schema to support these new parameters, including toggle flags to enable or disable each individual rule (e.g., `deviation`, `business_hours`, `max_quantity`).
- Modify the anomaly detection engine to evaluate all enabled rules sequentially or cumulatively, ensuring an anomaly is flagged if any rule is breached.
- If multiple rules are breached by the same movement, the system will log the reasons or aggregate the severity (e.g., business hours violation could be flagged as HIGH, while a massive quantity could be CRITICAL).

## Capabilities

### New Capabilities
<!-- Capabilities being introduced. -->

### Modified Capabilities

- `movement-analysis-rules`: Expanding the rule engine requirements to include business hours validation, max quantity validation, and individual rule toggles.

## Impact

- `anomaly_rules.yaml` configuration file structure will change.
- `AnomalyDetectionService` will need to implement the new validations.
- The `Anomaly` entity might need an updated `score` or description to indicate *which* rules were violated.
- Existing tests for the analysis service will need to be expanded to cover the new rule types.
