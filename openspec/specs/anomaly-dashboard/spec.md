# anomaly-dashboard Specification

## Purpose

Provides a visual interface for users to monitor supply chain anomalies, filter them by various dimensions, and access the system's API endpoints.

## Requirements

### Requirement: Anomaly Visualization

The dashboard SHALL display anomalies returned by the backend API.

#### Scenario: View anomalies

- **WHEN** the user accesses the dashboard
- **THEN** the system fetches the latest anomalies from the API and displays them in a data table or list format.

### Requirement: Interactive Filtering

The dashboard SHALL allow users to filter anomalies to focus on specific incidents.

#### Scenario: Filter by date range

- **WHEN** the user selects a specific time period in the filter controls
- **THEN** the dashboard updates to show only anomalies that occurred within the selected time range.

#### Scenario: Filter by severity

- **WHEN** the user selects a severity level (e.g., HIGH, CRITICAL)
- **THEN** the dashboard updates to show only anomalies matching the selected severity.

### Requirement: Dashboard Overview Metrics

The dashboard SHALL present high-level KPIs summarizing the current state of anomalies.

#### Scenario: View KPI cards

- **WHEN** the dashboard loads
- **THEN** it displays overview cards such as total anomalies in the period, breakdown by severity, and trend indicators.

### Requirement: Dark Theme and UX

The dashboard SHALL adhere to a dark theme and present an intuitive user experience.

#### Scenario: Load theme

- **WHEN** the user accesses the dashboard
- **THEN** it renders using a predefined dark theme configuration.

### Requirement: API Documentation Link

The dashboard SHALL include a prominent link to the backend API Swagger documentation.

#### Scenario: Navigate to Swagger

- **WHEN** the user clicks the API documentation link
- **THEN** they are redirected to the FastAPI Swagger UI to register movements or explore endpoints.
