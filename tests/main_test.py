import pytest
import app.main
from fastapi.testclient import TestClient

client = TestClient(app.main.fastapi)

def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}

def test_get_health2():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}

def test_list_models():
    response = client.get("/models/")
    assert response.status_code == 200
    assert "QL-500" in response.json()

def test_list_labels():
    response = client.get("/labels/")
    assert response.status_code == 200
    assert "62" in response.json()

