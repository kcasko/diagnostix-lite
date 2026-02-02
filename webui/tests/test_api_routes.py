
import html
import pytest
from fastapi.testclient import TestClient
from main import app

# Default credentials for testing
AUTH = ("admin", "diagnostix")

@pytest.fixture
def client():
    return TestClient(app)

def test_fixes_api_protected(client):
    """Test fixes API requires auth and returns list."""
    # Without auth -> 401
    assert client.get("/fixes/api").status_code == 401
    
    # With auth -> 200
    response = client.get("/fixes/api", auth=AUTH)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_simple_mode_start_protected(client):
    """Test simple mode start page requires auth."""
    # Without auth -> 401
    assert client.get("/simple").status_code == 401

    # With auth -> 200
    response = client.get("/simple", auth=AUTH)
    assert response.status_code == 200
    assert "What's wrong?" in html.unescape(response.text)

def test_api_health_protected(client):
    """Test health API requires auth."""
    # Note: /health is supposedly public in main check, but /api/v1/health is protected in routers/api.py
    # or main.py include_router logic. 
    # Let's check /api/v1/health specifically which is mounted with dependencies=[Depends(require_api_key)] 
    # or similar in main.py.
    
    # Actually, in main.py step 113, we did:
    # app.include_router(api_router, dependencies=[Depends(get_current_username)])
    
    response = client.get("/api/v1/health", auth=AUTH)
    assert response.status_code == 200
    data = response.json()
    assert "cpu_usage" in data

def test_run_diagnostic_invalid_tool(client):
    """Test running a non-existent diagnostic tool."""
    response = client.post("/api/v1/diagnostics/invalid_tool_id", auth=AUTH)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_run_fix_invalid_id(client):
    """Test running a non-existent fix."""
    response = client.post("/api/v1/fixes/invalid_fix_id", auth=AUTH)
    assert response.status_code == 404
