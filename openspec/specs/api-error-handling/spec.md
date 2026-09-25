# api-error-handling Specification

## Purpose
Padroniza as respostas de erro da API seguindo a RFC 7807 (Problem Details for HTTP APIs), melhorando a interoperabilidade e clareza para os clientes.

## Requirements

### Requirement: Standardize API error responses
The system SHALL return all application errors (such as validations, not found, conflicts, and business rules violations) structured according to RFC 7807.

#### Scenario: Business rule violation error
- **WHEN** an endpoint encounters a business rule violation (e.g., DomainError)
- **THEN** it returns a 400 Bad Request with a JSON body containing `type`, `title`, `status`, `detail`, and `instance` fields.

#### Scenario: Entity not found error
- **WHEN** a requested entity is not found
- **THEN** it returns a 404 Not Found with the standardized JSON structure.

#### Scenario: Validation error
- **WHEN** data validation fails
- **THEN** it returns a 422 Unprocessable Entity with the standardized JSON structure.

#### Scenario: Conflict error
- **WHEN** a resource conflict occurs (e.g., duplicate unique field)
- **THEN** it returns a 409 Conflict with the standardized JSON structure.
