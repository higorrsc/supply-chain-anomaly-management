# Spec Delta

## MODIFIED Requirements

### Requirement: YAML Configuration Structure

The system SHALL load anomaly detection rules from a YAML configuration file on startup. This configuration MUST define parameters such as acceptable deviation thresholds, business hours, maximum quantities, and individual rule enablement toggles.

#### Scenario: Parse valid configuration

- **WHEN** the system starts with a valid anomaly rules YAML file containing rules for deviation, business hours, and max quantity
- **THEN** the configuration is parsed and stored in memory for analysis
- **THEN** no startup errors are generated

#### Scenario: Handle malformed configuration

- **WHEN** the system starts but the anomaly rules YAML file is malformed or missing required keys for enabled rules
- **THEN** the application startup SHALL fail with a specific configuration error

### Requirement: Threshold Application

The system SHALL apply all enabled YAML rules to a given stock movement to determine if it violates thresholds. It MUST calculate an aggregated score and a severity level if any rules are breached.

#### Scenario: Movement exceeds statistical deviation

- **WHEN** a stock movement is analyzed and its deviation exceeds the configured critical threshold, and the deviation rule is enabled
- **THEN** the analysis returns a critical severity score

#### Scenario: Movement occurs outside business hours

- **WHEN** a stock movement occurs outside the configured business hours, and the business hours rule is enabled
- **THEN** the analysis flags the movement as an anomaly with the configured severity for time violations

#### Scenario: Movement exceeds max quantity

- **WHEN** an IN stock movement has a quantity greater than the configured IN limit, and the max quantity rule is enabled
- **THEN** the analysis flags the movement as an anomaly with the configured severity for quantity violations

#### Scenario: Movement stays within all safe boundaries

- **WHEN** a stock movement is analyzed and passes all enabled rules (deviation, time, and quantity)
- **THEN** the analysis returns no anomaly
