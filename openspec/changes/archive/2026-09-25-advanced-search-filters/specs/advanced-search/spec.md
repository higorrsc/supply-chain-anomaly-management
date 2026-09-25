# Spec Delta

## Purpose
Enables dynamic search filters, allowing partial matches (LIKE/ILIKE) on key text fields such as SKU and description, improving the usability of listing endpoints.

## ADDED Requirements

### Requirement: Support partial text matching in search
The system SHALL support partial text matching (e.g., ILIKE) when searching by designated string fields like `sku` and `description`.

#### Scenario: Searching by partial SKU
- **WHEN** a client requests a search with `sku` filter containing a partial string (e.g., "CEL-")
- **THEN** the system returns all records whose SKU contains that substring, ignoring case.

#### Scenario: Searching by partial description
- **WHEN** a client requests a search with `description` filter containing a partial string
- **THEN** the system returns all records whose description contains that substring.

### Requirement: Allow search by any entity field
The system SHALL accept search filters for any field present on the entity, falling back to exact match for non-textual fields or fields not explicitly designated for partial match.

#### Scenario: Exact match on boolean field
- **WHEN** a client requests a search with `is_active=true`
- **THEN** the system returns only active records, using an exact match.
