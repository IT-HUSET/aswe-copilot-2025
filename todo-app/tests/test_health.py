"""Tests for health endpoint."""

from datetime import datetime


def test_health_endpoint(client):
    """Test GET /health returns ok status and timestamp."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    
    # Verify timestamp is valid ISO format
    timestamp = datetime.fromisoformat(data["timestamp"])
    assert timestamp is not None
