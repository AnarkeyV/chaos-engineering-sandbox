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
    assert data["metrics"] == "/metrics"


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

    assert data["status"] in ["ready", "not_ready"]
    assert data["service"] == "chaos-api"
    assert "dependencies" in data
    assert "database" in data["dependencies"]
    assert "cache" in data["dependencies"]
    assert "timestamp" in data


def test_status_endpoint():
    response = client.get("/status")

    assert response.status_code == 200
    data = response.json()

    assert data["service"] == "chaos-api"
    assert data["version"] == "0.3.0"
    assert data["status"] == "running"
    assert data["features"]["observability"] is True
    assert data["features"]["chaos_experiments"] is True
    assert "dependencies" in data
    assert "timestamp" in data


def test_simulate_work_endpoint():
    response = client.get("/simulate-work")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Work simulation completed"
    assert data["status"] == "success"
    assert "processing_time_seconds" in data
    assert "timestamp" in data


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "chaos_api_http_requests_total" in response.text
    assert "chaos_api_http_request_duration_seconds" in response.text
    assert "chaos_api_http_requests_in_progress" in response.text