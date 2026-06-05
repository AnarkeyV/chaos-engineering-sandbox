from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Chaos Engineering Sandbox API"
    assert data["status"] == "running"
    assert data["docs"] == "/docs"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "chaos-api"
    assert "timestamp" in data


def test_ready_endpoint():
    response = client.get("/ready")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ready"
    assert data["service"] == "chaos-api"
    assert data["dependencies"]["database"] == "not_configured_yet"
    assert data["dependencies"]["cache"] == "not_configured_yet"


def test_status_endpoint():
    response = client.get("/status")

    assert response.status_code == 200
    data = response.json()

    assert data["service"] == "chaos-api"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "local"
    assert data["status"] == "running"
    assert data["features"]["database"] is False
    assert data["features"]["cache"] is False


def test_simulate_work_endpoint():
    response = client.get("/simulate-work")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Work simulation completed"
    assert data["status"] == "success"
    assert "processing_time_seconds" in data
    assert "timestamp" in data