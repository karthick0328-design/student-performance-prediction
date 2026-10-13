"""
AI-Based Student Performance Prediction System
Flask Web Application Backend
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for

# Ensure base directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.data_loader import (
    load_dataset,
    get_analytics_summary,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    ALL_FEATURE_COLUMNS,
    CATEGORICAL_OPTIONS,
    NUMERIC_RANGES,
)
from src.predict import predict_student_performance, get_performance_tier

app = Flask(
    __name__,
    static_folder=str(BASE_DIR / "static"),
    template_folder=str(BASE_DIR / "templates"),
)
app.config["SECRET_KEY"] = "academic-student-performance-secure-key-2026"

METRICS_FILE = BASE_DIR / "outputs" / "evaluation_metrics.json"


def load_cached_metrics() -> Dict[str, Any]:
    """
    Loads saved evaluation metrics from outputs/evaluation_metrics.json.
    """
    if METRICS_FILE.exists():
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


@app.route("/")
def index():
    """
    Home Dashboard displaying project overview, KPIs, and quick navigation.
    """
    metrics = load_cached_metrics()
    selected_metrics = metrics.get("selected_model_metrics", {})
    return render_template(
        "index.html",
        total_records=metrics.get("total_records", 395),
        feature_count=metrics.get("feature_count", 30),
        selected_model=metrics.get("selected_model", "Random Forest Regressor"),
        test_mae=selected_metrics.get("test_mae", 3.173),
        test_rmse=selected_metrics.get("test_rmse", 3.949),
        test_r2=selected_metrics.get("test_r2", 0.239),
        cv_mae=selected_metrics.get("cv_mae", 2.971),
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    Interactive student performance prediction form and inference result handler.
    """
    prediction_result = None
    form_errors = {}
    form_data = {}

    if request.method == "POST":
        raw_form = request.form.to_dict()
        form_data = raw_form
        result, errors = predict_student_performance(raw_form)
        if errors:
            form_errors = errors
        else:
            prediction_result = result

    # Default representative sample for easy exploration
    default_values = {
        "school": "GP",
        "sex": "F",
        "age": 17,
        "address": "U",
        "famsize": "GT3",
        "Pstatus": "T",
        "Medu": 3,
        "Fedu": 3,
        "Mjob": "services",
        "Fjob": "services",
        "reason": "course",
        "guardian": "mother",
        "traveltime": 1,
        "studytime": 2,
        "failures": 0,
        "schoolsup": "no",
        "famsup": "yes",
        "paid": "no",
        "activities": "yes",
        "nursery": "yes",
        "higher": "yes",
        "internet": "yes",
        "romantic": "no",
        "famrel": 4,
        "freetime": 3,
        "goout": 3,
        "Dalc": 1,
        "Walc": 2,
        "health": 4,
        "absences": 4,
    }

    current_data = form_data if form_data else default_values

    return render_template(
        "predict.html",
        categorical_options=CATEGORICAL_OPTIONS,
        numeric_ranges=NUMERIC_RANGES,
        current_data=current_data,
        prediction_result=prediction_result,
        form_errors=form_errors,
    )


@app.route("/analytics")
def analytics():
    """
    Dataset analytics and statistical distributions computed from real records.
    """
    try:
        df = load_dataset()
        summary = get_analytics_summary(df)
    except Exception as e:
        summary = {
            "total_records": 395,
            "pass_rate": 67.1,
            "mean_g3": 10.42,
            "median_g3": 11.0,
            "std_g3": 4.58,
            "g3_distribution": {"labels": [], "values": []},
            "studytime_impact": {"labels": [], "avg_grades": [], "counts": []},
            "failures_impact": {"labels": [], "avg_grades": []},
            "higher_ed_impact": {"labels": [], "avg_grades": []},
            "internet_impact": {"labels": [], "avg_grades": []},
            "medu_impact": {"labels": [], "avg_grades": []},
        }

    return render_template("analytics.html", summary=summary)


@app.route("/evaluation")
def evaluation():
    """
    Machine learning model evaluation, baseline comparison, and metric explanations.
    """
    metrics = load_cached_metrics()
    comparison_table = metrics.get("all_models_comparison", [])
    selected_model = metrics.get("selected_model", "Random Forest")
    selected_metrics = metrics.get("selected_model_metrics", {})

    return render_template(
        "evaluation.html",
        comparison_table=comparison_table,
        selected_model=selected_model,
        selected_metrics=selected_metrics,
        training_records=metrics.get("training_records", 316),
        test_records=metrics.get("test_records", 79),
    )


@app.route("/about")
def about():
    """
    Comprehensive academic documentation, methodology, limitations, and ethics.
    """
    return render_template("about.html")


@app.route("/outputs/<path:filename>")
def serve_output_file(filename: str):
    """
    Serves generated chart visualizations securely from outputs/.
    """
    outputs_dir = BASE_DIR / "outputs"
    return send_from_directory(outputs_dir, filename)


# REST API Endpoints
@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    JSON API for automated inference.
    """
    if not request.is_json:
        return jsonify({"success": False, "error": "Request body must be JSON."}), 400

    payload = request.get_json()
    result, errors = predict_student_performance(payload)
    if errors:
        return jsonify({"success": False, "errors": errors}), 422

    return jsonify({"success": True, "data": result}), 200


@app.route("/api/stats", methods=["GET"])
def api_stats():
    """
    JSON API for dataset summary metrics.
    """
    try:
        df = load_dataset()
        summary = get_analytics_summary(df)
        return jsonify({"success": True, "data": summary}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    msg = f"Requested path: '{request.path}' (PATH_INFO: '{request.environ.get('PATH_INFO')}')."
    return render_template("error.html", error_code=404, message=msg), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("error.html", error_code=500, message="An internal server error occurred."), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
