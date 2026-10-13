# Outputs Directory

This directory stores generated evaluation metrics, model comparison reports, and static visualization charts generated during the automated training run.

- `evaluation_metrics.json`: JSON report containing actual validation and test-set performance metrics for the baseline and all candidate models (MAE, RMSE, R²).
- `model_comparison.png`: Visual comparison of candidate algorithms across CV and Test MAE/R².
- `residuals_distribution.png`: Error analysis and prediction residual distribution on held-out test data.
- `feature_importance.png`: Top feature importances showing key factors influencing student academic achievement.
