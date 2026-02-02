
import os
import sys
from fastapi.testclient import TestClient

# Ensure we can import from current directory
sys.path.append(os.getcwd())

from main import app

client = TestClient(app)

# Hardcoded defaults matching implementation
DEFAULT_USER = "admin"
DEFAULT_PASS = "diagnostix"

def test_auth_missing():
    """Test access without credentials"""
    response = client.get("/")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Basic"

def test_auth_incorrect():
    """Test access with wrong credentials"""
    response = client.get("/", auth=("admin", "wrongpassword"))
    assert response.status_code == 401

def test_auth_correct_default():
    """Test access with default credentials"""
    response = client.get("/", auth=(DEFAULT_USER, DEFAULT_PASS))
    assert response.status_code == 200

def test_health_public():
    """Test that health check is PUBLIC (no auth)"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_api_protected():
    """Test that API routes are protected"""
    # /api/v1/diagnostics is a protected route
    response = client.get("/api/v1/diagnostics")
    assert response.status_code == 401
    
    response = client.get("/api/v1/diagnostics", auth=(DEFAULT_USER, DEFAULT_PASS))
    assert response.status_code == 200
