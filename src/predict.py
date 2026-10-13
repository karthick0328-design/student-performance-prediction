"""
Inference and Performance Prediction Module
AI-Based Student Performance Prediction System
"""

import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.preprocessing import validate_student_input
from src.data_loader import ALL_FEATURE_COLUMNS

MODEL_PATH = BASE_DIR / "models" / "student_model.joblib"

_CACHED_PIPELINE = None


def get_trained_pipeline():
    """
    Loads and caches the trained pipeline from disk.
    """
    global _CACHED_PIPELINE
    if _CACHED_PIPELINE is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Please run 'python src/train_model.py' first."
            )
        _CACHED_PIPELINE = joblib.load(MODEL_PATH)
    return _CACHED_PIPELINE


def get_performance_tier(score: float) -> Dict[str, str]:
    """
    Maps a predicted grade (0-20) to the standard Portuguese academic grading category.
    """
    rounded = round(score, 1)
    if rounded < 10.0:
        return {
            "tier": "Fail / At-Risk",
            "badge_class": "badge-danger",
            "grade_letter": "F",
            "summary": "At risk of failing the course (score < 10/20). Early academic intervention is strongly advised.",
        }
    elif rounded < 12.0:
        return {
            "tier": "Sufficient / Pass",
            "badge_class": "badge-warning",
            "grade_letter": "D",
            "summary": "Meets baseline passing threshold (10-11/20). Reinforcing study habits can boost stability.",
        }
    elif rounded < 14.0:
        return {
            "tier": "Satisfactory",
            "badge_class": "badge-info",
            "grade_letter": "C",
            "summary": "Solid average academic performance (12-13/20). Demonstrates consistent competency.",
        }
    elif rounded < 16.0:
        return {
            "tier": "Good",
            "badge_class": "badge-primary",
            "grade_letter": "B",
            "summary": "Strong academic standing (14-15/20). High potential for advanced academic achievement.",
        }
    elif rounded < 18.0:
        return {
            "tier": "Very Good",
            "badge_class": "badge-success",
            "grade_letter": "A-",
            "summary": "Very strong performance (16-17/20), exhibiting disciplined study habits and comprehension.",
        }
    else:
        return {
            "tier": "Excellent",
            "badge_class": "badge-success",
            "grade_letter": "A+",
            "summary": "Top-tier distinction (18-20/20), reflecting exceptional subject mastery.",
        }


def generate_recommendations(data: Dict[str, Any], predicted_score: float) -> list[str]:
    """
    Generates actionable educational recommendations based on input habits.
    """
    recs = []
    
    # Study time insights
    studytime = float(data.get("studytime", 2))
    if studytime <= 1:
        recs.append("Increase weekly study commitment: Currently studying <2 hours/week. Increasing to 2-5 hours significantly correlates with grade improvement.")
    elif studytime >= 3:
        recs.append("Positive habit: Strong weekly study commitment (>5 hours/week) provides a robust foundation for success.")

    # Failures insights
    failures = float(data.get("failures", 0))
    if failures > 0:
        recs.append(f"Past academic setbacks: Student has {int(failures)} past failure(s). Targeted tutoring and concept review can help bridge prerequisite knowledge gaps.")

    # Absences insights
    absences = float(data.get("absences", 0))
    if absences > 10:
        recs.append(f"High absence rate: {int(absences)} absences recorded. Class attendance directly correlates with consistent exam performance.")
    elif absences <= 2:
        recs.append("Excellent attendance record reinforces steady classroom learning.")

    # Extra educational support
    if data.get("schoolsup") == "yes":
        recs.append("Extra school support is active: Continue leveraging supplemental instruction sessions to consolidate core concepts.")
    
    # Higher education ambition
    if data.get("higher") == "no":
        recs.append("Career & higher education guidance: Aspiring to higher education strongly correlates with increased motivation and effort.")

    # Social and leisure balance
    goout = float(data.get("goout", 3))
    walc = float(data.get("Walc", 1))
    if goout >= 4 or walc >= 4:
        recs.append("Lifestyle balance: High weekend alcohol consumption or frequent socializing may encroach on revision and rest cycles.")

    if not recs:
        recs.append("Maintain the current balanced routine, consistent revision, and active classroom engagement.")

    return recs


def predict_student_performance(data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """
    Processes a raw input dictionary, runs inference through the trained pipeline,
    and returns a structured prediction payload.
    
    Args:
        data: Feature dictionary.
        
    Returns:
        Tuple[Dict[str, Any], Dict[str, str]]: (Result dictionary, errors dictionary)
    """
    df_clean, errors = validate_student_input(data)
    if errors:
        return {}, errors

    pipeline = get_trained_pipeline()
    raw_pred = pipeline.predict(df_clean)[0]
    
    # Clip to valid grade boundaries [0, 20]
    predicted_score = float(np.clip(raw_pred, 0.0, 20.0))
    tier_info = get_performance_tier(predicted_score)
    recommendations = generate_recommendations(data, predicted_score)

    result = {
        "predicted_grade": round(predicted_score, 2),
        "max_grade": 20,
        "percentage": round((predicted_score / 20.0) * 100, 1),
        "tier": tier_info["tier"],
        "grade_letter": tier_info["grade_letter"],
        "badge_class": tier_info["badge_class"],
        "tier_summary": tier_info["summary"],
        "recommendations": recommendations,
        "input_summary": df_clean.to_dict(orient="records")[0],
        "disclaimer": (
            "Educational Analytics Notice: Predictions represent statistical estimates "
            "based on historical demographic and behavioral data from the UCI dataset. "
            "They are intended for academic analysis and guidance, never as definitive "
            "or high-stakes judgments about an individual student's potential."
        ),
    }

    return result, {}
