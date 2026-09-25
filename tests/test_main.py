from fastapi.testclient import TestClient

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
    assert data["title"] == "HTTP Error"
    assert data["status"] == 404
    assert "00000000-0000-0000-0000-000000000000" in data["detail"]
    assert data["instance"] == "/api/v1/items/00000000-0000-0000-0000-000000000000"
