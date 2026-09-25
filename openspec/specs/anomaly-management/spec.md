# anomaly-management

## Purpose

Provides anomaly detection and management capabilities to process stock deviations, calculate scores, and manage anomaly alerts within the supply chain.

## Requirements

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

### Requirement: Generate Anomaly Alerts

The system SHALL generate an alert whenever an anomaly with 'HIGH' or 'CRITICAL' severity is registered. Alerts MUST be linked to the original anomaly.

#### Scenario: Alert generation for critical anomalies

- **WHEN** a 'CRITICAL' anomaly is registered
- **THEN** an Anomaly Alert is automatically generated and linked to the anomaly

#### Scenario: No alert for minor anomalies

- **WHEN** a 'LOW' anomaly is registered
- **THEN** no Anomaly Alert is generated

### Requirement: Resolve Anomaly

The system SHALL allow authorized users or processes to resolve an open anomaly. Resolving an anomaly MUST transition its status from 'OPEN' to 'RESOLVED'.

#### Scenario: Successfully resolving an anomaly

- **WHEN** an authorized user resolves an 'OPEN' anomaly
- **THEN** the anomaly status is updated to 'RESOLVED'

#### Scenario: Attempting to resolve an already resolved anomaly

- **WHEN** a user attempts to resolve a 'RESOLVED' anomaly
- **THEN** the system rejects the operation
