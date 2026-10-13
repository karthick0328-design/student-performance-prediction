"""
Integration tests for Flask application routes and REST API.
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Verify home dashboard loads with 200 OK and expected content."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Performance Prediction System" in response.data
    assert b"Random Forest" in response.data


def test_predict_page_get(client):
    """Verify prediction page GET loads form."""
    response = client.get("/predict")
    assert response.status_code == 200
    assert b"Student Information" in response.data
    assert b"studytime" in response.data


def test_predict_page_post_valid(client):
    """Verify valid form submission displays predicted score."""
    valid_payload = {
        "school": "GP", "sex": "F", "age": "17", "address": "U", "famsize": "GT3",
        "Pstatus": "T", "Medu": "3", "Fedu": "3", "Mjob": "services", "Fjob": "services",
        "reason": "course", "guardian": "mother", "traveltime": "1", "studytime": "2",
        "failures": "0", "schoolsup": "no", "famsup": "yes", "paid": "no",
        "activities": "yes", "nursery": "yes", "higher": "yes", "internet": "yes",
        "romantic": "no", "famrel": "4", "freetime": "3", "goout": "3", "Dalc": "1",
        "Walc": "2", "health": "4", "absences": "4",
    }
    response = client.post("/predict", data=valid_payload)
    assert response.status_code == 200
    assert b"Prediction Result" in response.data
    assert b"score-display" in response.data


def test_predict_page_post_invalid(client):
    """Verify invalid submission displays validation error alert."""
    invalid_payload = {"school": "GP", "sex": "F"}
    response = client.post("/predict", data=invalid_payload)
    assert response.status_code == 200
    assert b"Please check your inputs" in response.data


def test_analytics_page(client):
    """Verify analytics page loads charts and distributions."""
    response = client.get("/analytics")
    assert response.status_code == 200
    assert b"Data Analytics" in response.data
    assert b"chart-grade-dist" in response.data


def test_evaluation_page(client):
    """Verify evaluation page loads metrics and candidate benchmarks."""
    response = client.get("/evaluation")
    assert response.status_code == 200
    assert b"Model Evaluation" in response.data
    assert b"Random Forest" in response.data


def test_about_page(client):
    """Verify about page loads background and ethics documentation."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"Problem Statement" in response.data
    assert b"UCI Student Performance Dataset" in response.data


def test_api_predict_json(client):
    """Verify REST API /api/predict handles valid JSON requests."""
    payload = {
        "school": "GP", "sex": "M", "age": 16, "address": "U", "famsize": "LE3",
        "Pstatus": "T", "Medu": 4, "Fedu": 4, "Mjob": "teacher", "Fjob": "teacher",
        "reason": "reputation", "guardian": "father", "traveltime": 1, "studytime": 3,
        "failures": 0, "schoolsup": "no", "famsup": "yes", "paid": "yes",
        "activities": "yes", "nursery": "yes", "higher": "yes", "internet": "yes",
        "romantic": "no", "famrel": 5, "freetime": 2, "goout": 2, "Dalc": 1,
        "Walc": 1, "health": 5, "absences": 2,
    }
    response = client.post(
        "/api/predict",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "predicted_grade" in data["data"]


def test_api_predict_invalid_json(client):
    """Verify REST API /api/predict returns 422 on invalid payload."""
    invalid_payload = {"school": "INVALID"}
    response = client.post(
        "/api/predict",
        data=json.dumps(invalid_payload),
        content_type="application/json"
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data["success"] is False
    assert "errors" in data


def test_api_stats(client):
    """Verify /api/stats returns dataset aggregations."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "total_records" in data["data"]


def test_404_error_page(client):
    """Verify non-existent route returns 404 with custom error template."""
    response = client.get("/route-that-does-not-exist")
    assert response.status_code == 404
    assert b"Error 404" in response.data
