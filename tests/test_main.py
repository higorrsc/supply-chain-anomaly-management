from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from src.core.domain.exceptions import (
    ConflictError,
    DomainError,
    EntityNotFoundError,
    EntityValidationError,
)
from src.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Test the /health endpoint returns 200 OK and expected structure."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_rfc7807_error_format_on_not_found() -> None:
    """Test if a known not found route returns the RFC7807 format."""
    client = TestClient(app)
    response = client.get("/api/v1/items/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"

    data = response.json()
    assert data["type"] == "urn:api:error:not-found"
    assert data["title"] == "Not Found"
    assert data["status"] == 404
    assert "00000000-0000-0000-0000-000000000000" in data["detail"]
    assert data["instance"] == "/api/v1/items/00000000-0000-0000-0000-000000000000"


@app.get("/test-not-found")
def mock_route_not_found():
    raise EntityNotFoundError("Entity not found.")


@app.get("/test-conflict")
def mock_route_conflict():
    raise ConflictError("Entity already exists.")


@app.get("/test-validation")
def mock_route_validation():
    raise EntityValidationError("Validation failed.")


@app.get("/test-domain")
def mock_route_domain():
    raise DomainError("Domain rule violated.")


class DummyBody(BaseModel):
    name: str = Field(..., min_length=3)


@app.post("/test-request-validation")
def mock_route_req_validation(body: DummyBody):
    return body


def test_global_entity_not_found_handler():
    response = client.get("/test-not-found")
    assert response.status_code == 404
    data = response.json()
    assert data["type"] == "urn:api:error:not-found"
    assert "Entity not found" in data["detail"]


def test_global_conflict_error_handler():
    response = client.get("/test-conflict")
    assert response.status_code == 409
    data = response.json()
    assert data["type"] == "urn:api:error:conflict"
    assert "Entity already exists" in data["detail"]


def test_global_entity_validation_error_handler():
    response = client.get("/test-validation")
    assert response.status_code == 422
    data = response.json()
    assert data["type"] == "urn:api:error:validation"
    assert "Validation failed" in data["detail"]


def test_global_domain_error_handler():
    response = client.get("/test-domain")
    assert response.status_code == 400
    data = response.json()
    assert data["type"] == "urn:api:error:domain-rule-violation"
    assert "Domain rule violated" in data["detail"]


def test_global_request_validation_handler():
    response = client.post("/test-request-validation", json={"name": "a"})
    assert response.status_code == 422
    data = response.json()
    assert data["type"] == "urn:api:error:validation"

def test_global_http_exception_handler():
    response = client.get("/invalid-route-does-not-exist")
    assert response.status_code == 404
    data = response.json()
    assert data["type"] == "urn:api:error:not-found"
    assert data["title"] == "HTTP Error"
