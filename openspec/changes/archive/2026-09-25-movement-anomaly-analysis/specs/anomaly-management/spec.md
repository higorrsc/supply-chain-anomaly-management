# Spec Delta

## MODIFIED Requirements

### Requirement: Detect and Register Anomaly

The system SHALL automatically analyze stock movements for deviations immediately after they are registered (e.g., via domain events). If the analysis, using the configured dynamic rules, calculates a deviation score that warrants an anomaly, the system SHALL register an anomaly. The anomaly MUST default to an 'OPEN' status, and the system MUST assign a severity level based on the analysis.

#### Scenario: Registering a high severity anomaly upon movement creation

- **WHEN** a stock movement event is processed and the analysis score exceeds the critical configuration threshold
- **THEN** the anomaly is created automatically with 'CRITICAL' severity linked to the movement
- **THEN** the anomaly status is set to 'OPEN'

#### Scenario: Registering a low severity anomaly upon movement creation

- **WHEN** a stock movement event is processed and the analysis score falls in the lowest configured deviation bracket
- **THEN** the anomaly is created automatically with 'LOW' severity linked to the movement
- **THEN** the anomaly status is set to 'OPEN'

#### Scenario: Normal movement does not create anomaly

- **WHEN** a stock movement event is processed and stays within safe bounds according to the rules
- **THEN** no anomaly is registered
