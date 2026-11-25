from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "project": "PY-W4-004"}

def test_openapi_documentation_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/employees" in response.json()["paths"]
