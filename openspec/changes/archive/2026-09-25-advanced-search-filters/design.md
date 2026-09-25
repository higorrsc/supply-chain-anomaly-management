# Design

## Context

The `search` method in `SqlAlchemyRepository` currently applies filters dynamically using an exact match `column == value`. However, to provide flexibility in text search (like SKU and description), the repository should support case-insensitive wildcard searches (ILIKE in Postgres) without losing the generic support for other fields (like UUIDs, booleans, and numbers).

## Goals / Non-Goals

**Goals:**
- Allow the API to receive text fields and translate them into `ILIKE %value%` database queries.
- Enable search endpoints (like Items) to accept any partial substring for SKU or description.

**Non-Goals:**
- Implement "full-text search" (like tsvector/ElasticSearch).
- Implement custom operators (greater than, less than) in this change (only exact match and textual ILIKE).

## Decisions

- **Column type identification**: When iterating over the filters dictionary in `SqlAlchemyRepository.search()`, the code will inspect the ORM column type (via `isinstance(column.type, String)` or similar SQLAlchemy attributes). If the table field is textual (String) and the searched value is text, the applied filter will be a case-insensitive partial search: `stmt.where(column.ilike(f"%{value}%"))`. Otherwise, it will fallback to `column == value`.
  - **Rejected alternative:** Pass operators in the DTO itself (e.g., `{"description__ilike": "celular"}`). While more flexible, this would break the simplicity of the DDD application/domain layer, leaking query details. Deducing the operator by column data type provides a "plug-and-play" behavior.
- **Controllers and Use Cases Update**: Ensure that the `description` field is received as an optional query parameter in the items search API (currently it only receives `sku` and `is_active`), so the client can filter by parts of the description.

## Risks / Trade-offs

- **ILIKE Performance**: Searches using `ILIKE %value%` generally cannot use b-tree indexes (except for gin/gist indexes in Postgres with trigrams). For the context and expected data volume initially, this is acceptable, but it may represent a slowdown in the future.
  - *Mitigation*: If performance degrades after millions of records, it will be necessary to introduce `pg_trgm`.
