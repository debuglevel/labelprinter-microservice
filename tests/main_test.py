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


def get_valid_print_json():
    return {
        "image_url":
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/Resistor_symbol_IEC.svg",
        "red": False,
        "low_quality": False,
        "high_dpi": False,
        "compress": False,
        "printer_url": "tcp://127.0.0.1:9100",
        "printer_backend": "network",
        "printer_model": "QL-500",
        "label_type": "62",
        "description": "Whatever"
    }


def test_post_prints_with_invalid_model():
    json = get_valid_print_json()
    json["printer_model"] = "INVALID_MODEL"

    response = client.post("/prints/", json=json)
    assert response.status_code == 400
    assert "INVALID_MODEL" in response.text


def test_post_prints_with_invalid_label():
    json = get_valid_print_json()
    json["label_type"] = "INVALID_LABEL"

    response = client.post("/prints/", json=json)
    assert response.status_code == 400
    assert "INVALID_LABEL" in response.text
