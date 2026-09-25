# Proposal

## Why

We need to expose the `anomaly` bounded context features through an HTTP API. This will allow external clients (or a frontend) to register anomalies, resolve them, and query them. 

## What Changes

- Create Pydantic schemas for the API input and output payloads (e.g., `AnomalyResponse`, `RegisterAnomalyRequest`) in `src/anomaly/presentation/api/schemas/`.
- Create FastAPI routers/controllers in `src/anomaly/presentation/api/controllers/` exposing the endpoints for:
  - `POST /anomalies`
  - `GET /anomalies/{anomaly_id}`
  - `GET /anomalies`
  - `PUT /anomalies/{anomaly_id}/resolve`
  - `GET /anomalies/{anomaly_id}/alerts`
- Create FastAPI dependencies (e.g., database session provider, repository instantiation) in `src/anomaly/presentation/api/dependencies.py` (if applicable) or use existing ones from the core.

## Capabilities

### New Capabilities

- `<none>`

### Modified Capabilities

- `<none>`

## Impact

This will create the first API endpoints for the `anomaly` context. It requires FastAPI to be properly configured to include these routers (either directly or via an API Gateway setup).
