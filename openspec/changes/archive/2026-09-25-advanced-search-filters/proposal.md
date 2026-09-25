# Proposal

## Why

Currently, the default search mechanism (`GenericSearchUseCase` and `SqlAlchemyRepository.search`) supports only exact filters based on direct column-value mapping (using `==`). To provide a better user experience, we need to allow text fields (like `description` and `sku`) to be filtered by partial matches (using `ILIKE` or equivalent) and ensure all entity fields can be exposed for filtering.

## What Changes

- Modify the search logic in the generic repository (`SqlAlchemyRepository.search`) to inspect column types and apply `ILIKE` for text fields allowing partial search.
- Update API Controllers and Use Cases to expose advanced search parameters where applicable, allowing clients to search by partial SKU and description in contexts that have these properties.

## Capabilities

### New Capabilities
- `advanced-search`: Support for dynamic search filters, including the ability to perform partial searches (LIKE/ILIKE) on key text fields such as SKU and description.

### Modified Capabilities
None.

## Impact

- Affects `SqlAlchemyRepository.search` in the `core` module.
- Affects `SearchRequestDTO` or controllers to pass the additional query parameters.
- Should not break existing exact searches for fields that don't use wildcards, but requires testing to ensure backwards compatibility.
