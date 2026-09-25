# anomaly-management

## Purpose

Provides anomaly detection and management capabilities to process stock deviations, calculate scores, and manage anomaly alerts within the supply chain.

## Requirements

### Requirement: Detect and Register Anomaly

The system SHALL register an anomaly for a given stock deviation with a calculated deviation score. The anomaly MUST default to an 'OPEN' status. The system MUST assign a severity level based on the deviation score thresholds.

#### Scenario: Registering a high severity anomaly

- **WHEN** a stock deviation is detected with a score above the critical threshold
- **THEN** the anomaly is created with 'CRITICAL' severity
- **THEN** the anomaly status is set to 'OPEN'

#### Scenario: Registering a low severity anomaly

- **WHEN** a stock deviation is detected with a score in the lowest deviation bracket
- **THEN** the anomaly is created with 'LOW' severity
- **THEN** the anomaly status is set to 'OPEN'

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
