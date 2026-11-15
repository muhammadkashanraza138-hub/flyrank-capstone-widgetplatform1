from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_widget_javascript_endpoint():
    response = client.get("/widget.js")
    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]
    assert len(response.content) > 0


def test_widget_javascript_cache_header():
    response = client.get("/widget.js")
    assert response.headers["cache-control"] == (
        "public, max-age=31536000, immutable"
    )
