"""
Model Evaluation and Metric Calculation Module
AI-Based Student Performance Prediction System
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib
matplotlib.use("Agg")  # Headless backend for server/script plotting
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculates standard regression performance metrics.
    
    Args:
        y_true: Ground truth target values.
        y_pred: Predicted values.
        
    Returns:
        Dict[str, float]: Dictionary with MAE, RMSE, and R2.
    """
    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true, y_pred))
    return {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
    }


def plot_model_comparison(results_df: pd.DataFrame, output_path: str) -> None:
    """
    Plots cross-validation and test set MAE comparison across models.
    """
    plt.figure(figsize=(9, 5))
    x = np.arange(len(results_df))
    width = 0.35

    plt.bar(x - width / 2, results_df["cv_mae"], width, label="CV MAE (5-Fold)", color="#3b82f6")
    plt.bar(x + width / 2, results_df["test_mae"], width, label="Test Set MAE", color="#10b981")

    plt.xlabel("Candidate Models", fontsize=11, fontweight="bold")
    plt.ylabel("Mean Absolute Error (Grade Points)", fontsize=11, fontweight="bold")
    plt.title("Model Comparison: 5-Fold CV vs. Test Set MAE", fontsize=13, fontweight="bold", pad=12)
    plt.xticks(x, results_df["model"], rotation=15, ha="right")
    plt.legend(frameon=True)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_residuals(y_true: np.ndarray, y_pred: np.ndarray, output_path: str) -> None:
    """
    Plots residual distribution and predicted vs. actual values.
    """
    residuals = y_true - y_pred
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Scatter of True vs Predicted
    ax1.scatter(y_true, y_pred, alpha=0.6, color="#2563eb", edgecolors="none")
    ax1.plot([0, 20], [0, 20], "r--", linewidth=1.5, label="Perfect 1:1 Fit")
    ax1.set_xlabel("Actual Grade (0-20)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Predicted Grade (0-20)", fontsize=10, fontweight="bold")
    ax1.set_title("Actual vs. Predicted Final Grade (Test Set)", fontsize=11, fontweight="bold")
    ax1.set_xlim(-1, 21)
    ax1.set_ylim(-1, 21)
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.5)

    # Residuals Histogram
    sns.histplot(residuals, kde=True, ax=ax2, color="#0d9488", bins=15)
    ax2.axvline(0, color="red", linestyle="--", linewidth=1.5)
    ax2.set_xlabel("Residual (Actual - Predicted)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Frequency", fontsize=10, fontweight="bold")
    ax2.set_title("Residual Error Distribution", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_feature_importance(pipeline: Any, feature_names: list, output_path: str) -> None:
    """
    Extracts and plots feature importances for tree-based pipeline models.
    """
    model = pipeline.named_steps.get("model")
    if hasattr(model, "feature_importances_"):
        # Extract transformed feature names from ColumnTransformer
        preprocessor = pipeline.named_steps["prep"]
        encoded_cat_names = preprocessor.named_transformers_["cat"].get_feature_names_out()
        all_encoded_names = list(preprocessor.transformers[0][2]) + list(encoded_cat_names)
        
        importances = model.feature_importances_
        fi_df = pd.DataFrame({"feature": all_encoded_names, "importance": importances})
        fi_df = fi_df.sort_values(by="importance", ascending=False).head(15)

        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=fi_df,
            x="importance",
            y="feature",
            hue="feature",
            palette="Blues_r",
            legend=False,
        )
        plt.xlabel("Gini Feature Importance", fontsize=11, fontweight="bold")
        plt.ylabel("Transformed Feature", fontsize=11, fontweight="bold")
        plt.title("Top 15 Most Influential Features (Random Forest)", fontsize=13, fontweight="bold", pad=12)
        plt.grid(axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(output_path, dpi=200)
        plt.close()
