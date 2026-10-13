"""
Unit tests for model loading and prediction inference.
"""

import pytest
from src.predict import (
    get_trained_pipeline,
    predict_student_performance,
    get_performance_tier,
)


@pytest.fixture
def sample_valid_student():
    return {
        "school": "GP", "sex": "M", "age": 16, "address": "U", "famsize": "LE3",
        "Pstatus": "T", "Medu": 4, "Fedu": 4, "Mjob": "teacher", "Fjob": "teacher",
        "reason": "reputation", "guardian": "father", "traveltime": 1, "studytime": 3,
        "failures": 0, "schoolsup": "no", "famsup": "yes", "paid": "yes",
        "activities": "yes", "nursery": "yes", "higher": "yes", "internet": "yes",
        "romantic": "no", "famrel": 5, "freetime": 2, "goout": 2, "Dalc": 1,
        "Walc": 1, "health": 5, "absences": 2,
    }


def test_pipeline_loading():
    """Verify saved pipeline loads and has expected named steps."""
    pipeline = get_trained_pipeline()
    assert "prep" in pipeline.named_steps
    assert "model" in pipeline.named_steps


def test_prediction_output_structure(sample_valid_student):
    """Verify inference returns valid score within 0-20 bounds and required fields."""
    result, errors = predict_student_performance(sample_valid_student)
    assert len(errors) == 0
    assert "predicted_grade" in result
    assert "tier" in result
    assert "grade_letter" in result
    assert "recommendations" in result
    assert 0.0 <= result["predicted_grade"] <= 20.0
    assert 0.0 <= result["percentage"] <= 100.0


def test_prediction_tiers():
    """Verify grade tier boundaries."""
    assert get_performance_tier(8.5)["tier"] == "Fail / At-Risk"
    assert get_performance_tier(10.5)["tier"] == "Sufficient / Pass"
    assert get_performance_tier(13.0)["tier"] == "Satisfactory"
    assert get_performance_tier(15.0)["tier"] == "Good"
    assert get_performance_tier(17.0)["tier"] == "Very Good"
    assert get_performance_tier(19.0)["tier"] == "Excellent"


def test_prediction_edge_cases(sample_valid_student):
    """Verify high-risk student input generates appropriate warnings."""
    at_risk_student = sample_valid_student.copy()
    at_risk_student["failures"] = 3
    at_risk_student["studytime"] = 1
    at_risk_student["absences"] = 25
    at_risk_student["higher"] = "no"

    result, errors = predict_student_performance(at_risk_student)
    assert len(errors) == 0
    assert 0.0 <= result["predicted_grade"] <= 20.0
    # Ensure tailored recommendations are generated
    rec_text = " ".join(result["recommendations"])
    assert "failure" in rec_text.lower()
    assert "study" in rec_text.lower()

