# Spec Delta

## Purpose

Provides configurable rules for analyzing stock movements, allowing dynamic thresholds and parameters without code changes.

## ADDED Requirements

### Requirement: YAML Rule Configuration Loading

The system SHALL load anomaly detection rules from a YAML configuration file on startup. This configuration MUST define parameters such as acceptable deviation thresholds and moving average configurations.

#### Scenario: Successfully loading a valid YAML configuration

- **WHEN** the system starts with a valid anomaly rules YAML file present
- **THEN** the configuration is parsed and stored in memory for analysis
- **THEN** no startup errors are generated

#### Scenario: Fails to start on invalid configuration

- **WHEN** the system starts but the anomaly rules YAML file is malformed or missing
- **THEN** the application startup SHALL fail with a specific configuration error

### Requirement: Apply Rules to Movement

The system SHALL apply the loaded YAML rules to a given stock movement to determine if it violates thresholds. It MUST calculate a score and a severity level if rules are breached.

#### Scenario: Rule application detects high severity

- **WHEN** a stock movement is analyzed and its deviation exceeds the configured critical threshold
- **THEN** the analysis returns a critical severity score

#### Scenario: Rule application detects normal behavior

- **WHEN** a stock movement is analyzed and stays within the configured safe boundaries
- **THEN** the analysis returns no anomaly
