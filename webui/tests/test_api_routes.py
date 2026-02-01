from fastapi.testclient import TestClient
from main import app


def test_fixes_api():
    client = TestClient(app)
    response = client.get("/fixes/api")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_simple_mode_start():
    client = TestClient(app)
    response = client.get("/simple")
    assert response.status_code == 200
    assert "What's wrong?" in response.text
