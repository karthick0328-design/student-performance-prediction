"""
Model Training and Orchestration Script
AI-Based Student Performance Prediction System
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.data_loader import load_dataset, get_feature_target_split, ALL_FEATURE_COLUMNS
from src.preprocessing import build_preprocessor
from src.evaluate_model import (
    calculate_metrics,
    plot_model_comparison,
    plot_residuals,
    plot_feature_importance,
)

MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"


def train_and_evaluate_pipeline() -> Dict[str, Any]:
    """
    Executes the full machine learning training, cross-validation, selection,
    and test-set evaluation pipeline.
    """
    MODELS_DIR.mkdir(exist_ok=True)
    OUTPUTS_DIR.mkdir(exist_ok=True)

    print("Step 1: Loading and validating dataset...")
    df = load_dataset()
    print(f"Dataset successfully loaded. Total records: {len(df)}, Columns: {len(df.columns)}")

    X, y = get_feature_target_split(df)
    print(f"Features: {X.shape[1]} columns (Excluded G1 and G2 to prevent target leakage).")

    print("\nStep 2: Splitting dataset into training (80%) and held-out test (20%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training instances: {len(X_train)}, Held-out test instances: {len(X_test)}")

    preprocessor = build_preprocessor()

    # Candidate models definition
    candidates = {
        "Baseline (Mean)": DummyRegressor(strategy="mean"),
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=10.0, random_state=42),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            min_samples_split=5,
            random_state=42,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=80,
            max_depth=3,
            learning_rate=0.05,
            random_state=42,
        ),
    }

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    comparison_records = []
    trained_pipelines = {}

    print("\nStep 3: Evaluating candidate models using 5-Fold Cross-Validation on training set...")
    for name, model in candidates.items():
        pipe = Pipeline(steps=[("prep", preprocessor), ("model", model)])
        
        # Calculate CV MAE and R2 strictly on X_train, y_train
        cv_mae_scores = -cross_val_score(
            pipe, X_train, y_train, cv=cv, scoring="neg_mean_absolute_error"
        )
        cv_r2_scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="r2")
        cv_mae = float(np.mean(cv_mae_scores))
        cv_r2 = float(np.mean(cv_r2_scores))

        # Train on entire training set
        pipe.fit(X_train, y_train)
        trained_pipelines[name] = pipe

        # Evaluate on held-out test set
        test_preds = pipe.predict(X_test)
        test_metrics = calculate_metrics(y_test.values, test_preds)

        comparison_records.append({
            "model": name,
            "cv_mae": round(cv_mae, 4),
            "cv_r2": round(cv_r2, 4),
            "test_mae": test_metrics["mae"],
            "test_rmse": test_metrics["rmse"],
            "test_r2": test_metrics["r2"],
        })

        print(
            f"  -> {name:<20}: CV MAE = {cv_mae:.3f} | CV R2 = {cv_r2:.3f} | "
            f"Test MAE = {test_metrics['mae']:.3f} | Test RMSE = {test_metrics['rmse']:.3f} | "
            f"Test R2 = {test_metrics['r2']:.3f}"
        )

    comparison_df = pd.DataFrame(comparison_records)

    # Select the model with the lowest CV MAE (Random Forest)
    # Exclude Baseline from selection
    candidate_records = [r for r in comparison_records if r["model"] != "Baseline (Mean)"]
    best_candidate = min(candidate_records, key=lambda x: x["cv_mae"])
    selected_name = best_candidate["model"]
    selected_pipeline = trained_pipelines[selected_name]

    print(f"\nStep 4: Selected Best Model based on validation: '{selected_name}'")

    # Serialize best pipeline
    model_path = MODELS_DIR / "student_model.joblib"
    joblib.dump(selected_pipeline, model_path)
    print(f"Saved selected model pipeline to: {model_path}")

    # Final test evaluation metrics of selected model
    final_test_preds = selected_pipeline.predict(X_test)
    final_test_metrics = calculate_metrics(y_test.values, final_test_preds)

    # Compile comprehensive report
    report = {
        "dataset_name": "UCI Student Performance (Math Course)",
        "total_records": len(df),
        "training_records": len(X_train),
        "test_records": len(X_test),
        "feature_count": len(ALL_FEATURE_COLUMNS),
        "features": ALL_FEATURE_COLUMNS,
        "target_variable": "G3",
        "target_range": [0, 20],
        "excluded_features": ["G1", "G2"],
        "selected_model": selected_name,
        "selected_model_metrics": {
            "cv_mae": best_candidate["cv_mae"],
            "cv_r2": best_candidate["cv_r2"],
            "test_mae": final_test_metrics["mae"],
            "test_rmse": final_test_metrics["rmse"],
            "test_r2": final_test_metrics["r2"],
        },
        "all_models_comparison": comparison_records,
    }

    # Save metrics JSON
    metrics_path = OUTPUTS_DIR / "evaluation_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Saved evaluation metrics to: {metrics_path}")

    # Generate visualization artifacts
    print("\nStep 5: Generating evaluation plots...")
    plot_model_comparison(comparison_df, str(OUTPUTS_DIR / "model_comparison.png"))
    plot_residuals(y_test.values, final_test_preds, str(OUTPUTS_DIR / "residuals_distribution.png"))
    plot_feature_importance(selected_pipeline, ALL_FEATURE_COLUMNS, str(OUTPUTS_DIR / "feature_importance.png"))
    print("All charts successfully generated in outputs/")

    return report


if __name__ == "__main__":
    train_and_evaluate_pipeline()
