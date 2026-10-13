# AI-Based Student Performance Prediction System

An end-to-end, production-grade Educational Data Mining (EDM) machine learning web application. The system analyzes student socio-demographic, familial, and study habit indicators to predict final academic achievement (`G3`, 0–20 scale), identify at-risk learners early, and deliver actionable guidance without target data leakage.

---

## 📌 Project Overview

- **Task Type:** Supervised Machine Learning Regression (Final Grade $G3 \in [0, 20]$) + Portuguese Academic Performance Categorization.
- **Dataset:** UC Irvine Machine Learning Repository — Student Performance Data Set (*Cortez & Silva, 2008*).
- **Core Algorithm:** Regularized **Random Forest Regressor** (5-Fold Cross-Validation on training data).
- **Data Leakage Prevention:** Intermediate exam scores ($G1$ and $G2$) are strictly excluded from the feature space, enabling genuine early-intervention before periodic evaluations occur.
- **Evaluation Split:** 80% Train ($n=316$), 20% Held-Out Test ($n=79$) with fixed seed ($42$).

---

## 🏆 Model Performance Summary (Held-Out Test Set)

| Model Candidate | 5-Fold CV MAE | 5-Fold CV R² | Test Set MAE | Test Set RMSE | Test Set R² | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Selected)** | **2.971** | **0.208** | **3.173** | **3.949** | **0.239** | **Deployed** |
| Gradient Boosting | 3.052 | 0.198 | 3.171 | 3.929 | 0.247 | Candidate |
| Ridge Regression ($\alpha=10.0$) | 3.417 | -0.016 | 3.374 | 4.180 | 0.148 | Candidate |
| Linear Regression (OLS) | 3.523 | -0.092 | 3.395 | 4.196 | 0.141 | Candidate |
| Baseline (Dummy Mean) | 3.403 | -0.035 | 3.646 | 4.550 | -0.010 | Benchmark |

*All metrics are calculated directly from authentic UCI student records; no invented or hardcoded metrics.*

---

## 🏗️ Repository Architecture

```text
student-performance-prediction/
├── app.py                             # Flask web server & REST API
├── requirements.txt                   # Pinned project dependencies
├── pytest.ini                         # Automated test suite configuration
├── student_performance_analysis.ipynb # Fully executed Jupyter analysis notebook
├── README.md                          # Comprehensive setup & documentation
├── PROJECT_REPORT.md                  # Academic report for formal submission
├── data/
│   ├── README.md                      # Feature dictionary & source attribution
│   ├── student-mat.csv                # Primary math course dataset (395 records)
│   ├── student-por.csv                # Portuguese language dataset (649 records)
│   └── student.txt                    # Raw UCI attribute descriptions
├── models/
│   ├── README.md                      # Model serialization documentation
│   └── student_model.joblib           # Serialized preprocessor + Random Forest pipeline
├── src/
│   ├── data_loader.py                 # Ingestion, validation, and analytics aggregation
│   ├── preprocessing.py               # ColumnTransformer pipeline and input validators
│   ├── train_model.py                 # 5-Fold CV, model selection, and artifact generation
│   ├── evaluate_model.py              # Regression metrics, residual and importance plots
│   └── predict.py                     # Inference engine, performance tiers & guidance
├── templates/
│   ├── base.html                      # Layout template with responsive sidebar
│   ├── index.html                     # Home dashboard with KPIs and shortcuts
│   ├── predict.html                   # 30-feature prediction form & result card
│   ├── analytics.html                 # Empirical distribution and correlation charts
│   ├── evaluation.html                # Model comparison benchmarks & diagnostic plots
│   ├── about.html                     # Academic problem statement, ethics & future scope
│   └── error.html                     # Custom 404 / 500 error display
├── static/
│   ├── css/
│   │   └── style.css                  # Professional academic & analytics UI design system
│   └── js/
│       └── main.js                    # Client-side input validation and form reset
├── tests/
│   ├── test_preprocessing.py          # Data loading, leakage prevention & validation tests
│   ├── test_prediction.py             # Pipeline inference, bounds & edge cases tests
│   └── test_routes.py                 # Web routes, REST endpoints & error handler tests
└── outputs/
    ├── README.md                      # Generated outputs guide
    ├── evaluation_metrics.json        # Serialized evaluation metrics (CV & test)
    ├── model_comparison.png           # CV vs. Test MAE comparison chart
    ├── residuals_distribution.png     # Residual error and scatter diagnostics
    └── feature_importance.png         # Top 15 Random Forest feature importances
```

---

## 🚀 Windows Setup and Run Instructions

### 1. Prerequisites
- **Operating System:** Windows 10 or 11
- **Python:** Python 3.11+ or 3.12+ installed and added to `PATH`.

### 2. Open PowerShell or Command Prompt
Navigate to the project root directory:
```powershell
Set-Location "E:\Student Prediction"
```

### 3. Create & Activate a Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(On standard Command Prompt, run `.\.venv\Scripts\activate.bat`)*

### 4. Install Dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Train the Machine Learning Pipeline
This trains all candidate algorithms, executes 5-fold cross-validation, selects the best model, calculates held-out test metrics, serializes `models/student_model.joblib`, and outputs visual diagnostic charts in `outputs/`:
```powershell
python src/train_model.py
```

### 6. Run the Automated Test Suite
Execute the comprehensive Pytest suite (21 unit and integration tests):
```powershell
python -m pytest -v
```

### 7. Run the Analysis Notebook
To inspect or rerun the Jupyter notebook:
```powershell
jupyter notebook student_performance_analysis.ipynb
```
*(Note: `student_performance_analysis.ipynb` has already been pre-executed with all output plots and tables populated.)*

### 8. Start the Flask Web Application
```powershell
python app.py
```
Open your web browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## 🌐 Application Pages Overview

1. **Dashboard (`/`):** Key performance indicators (Total records, feature count, deployed model, test MAE, RMSE, and R²), architectural highlights, and quick navigation.
2. **Predict Performance (`/predict`):** Comprehensive input form with 30 validated attributes (demographics, familial background, study habits, health, and lifestyle). Submitting displays:
   - Predicted final grade out of 20 points
   - Percentage conversion
   - Portuguese academic performance category (e.g., *Satisfactory*, *Good*, *At-Risk*)
   - Personalized educational recommendations
3. **Data Analytics (`/analytics`):** Real-time interactive charts generated directly from dataset records (Grade distributions, study hours impact, failure penalties, motivation indicators).
4. **Model Evaluation (`/evaluation`):** Empirical candidate benchmarking table, diagnostic residual plots, Gini feature importance chart, and metric definitions.
5. **About (`/about`):** Academic context, methodology, data attribution, system limitations, and ethical considerations.

---

## 📡 REST API Documentation

### Predict Endpoint
- **URL:** `/api/predict`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Payload Example:**
```json
{
  "school": "GP", "sex": "F", "age": 17, "address": "U", "famsize": "GT3",
  "Pstatus": "T", "Medu": 3, "Fedu": 3, "Mjob": "services", "Fjob": "services",
  "reason": "course", "guardian": "mother", "traveltime": 1, "studytime": 2,
  "failures": 0, "schoolsup": "no", "famsup": "yes", "paid": "no",
  "activities": "yes", "nursery": "yes", "higher": "yes", "internet": "yes",
  "romantic": "no", "famrel": 4, "freetime": 3, "goout": 3, "Dalc": 1,
  "Walc": 2, "health": 4, "absences": 4
}
```
- **Response (`200 OK`):**
```json
{
  "success": true,
  "data": {
    "predicted_grade": 12.8,
    "max_grade": 20,
    "percentage": 64.0,
    "tier": "Satisfactory",
    "grade_letter": "C",
    "badge_class": "badge-info",
    "recommendations": [
      "Maintain the current balanced routine, consistent revision, and active classroom engagement."
    ],
    "disclaimer": "Educational Analytics Notice: Predictions represent statistical estimates..."
  }
}
```

---

## ⚖️ Ethical Considerations & Educational Disclaimer

> **Important Notice:** Model predictions are statistical estimates derived from historical demographic and behavioral data from Portuguese secondary schools (Cortez & Silva, 2008). They are intended strictly for educational research and constructive early guidance. They must **never** be used for high-stakes academic evaluations, tracking students into restricted curricula, or penalizing individual learners.
