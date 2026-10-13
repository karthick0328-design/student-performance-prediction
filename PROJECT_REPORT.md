# Project Report: AI-Based Student Performance Prediction System

**Academic Project Report**  
**Course / Discipline:** Computer Science, Machine Learning & Educational Data Mining  
**Target Platform:** Windows Native / Local Web Environment  

---

## Abstract

Academic underperformance in secondary education often goes undetected until summative final examinations, limiting the window for effective remedial intervention. This project develops an end-to-end, reproducible Machine Learning (ML) system designed to predict final secondary school academic achievement ($G3 \in [0, 20]$) based on socio-demographic, familial, and lifestyle behavioral indicators. Utilizing the canonical UC Irvine Student Performance dataset ($n=395$), the data preprocessing pipeline standardizes numeric features and one-hot encodes categorical dimensions while strictly excluding intermediate period grades ($G1$ and $G2$) to prevent target data leakage and ensure authentic early-warning utility. Five candidate algorithms—Baseline Mean Regressor, Ordinary Least Squares Linear Regression, L2 Regularized Ridge Regression, Random Forest Regressor, and Gradient Boosting Regressor—were evaluated using 5-fold cross-validation on an 80% training partition ($n=316$). The regularized Random Forest model attained the highest cross-validation score ($\text{MAE} = 2.971$, $R^2 = 0.208$) and demonstrated strong generalization on the held-out 20% test partition ($n=79$) with an MAE of 3.173 and RMSE of 3.949. The model was serialized into an immutable scikit-learn pipeline and deployed within a Flask-based web application featuring an interactive 30-feature prediction interface, empirical cohort analytics, model diagnostic visualizations, and an automated REST API. A 21-test Pytest test suite guarantees 100% test passing coverage across data loading, transformation, inference bounds, and web endpoints.

---

## 1. Problem Statement

Secondary education serves as a pivotal bridge to tertiary studies and future professional trajectories. However, traditional educational assessment mechanisms rely heavily on summative milestones (such as midterm and final exams). By the time poor grades are recorded, students frequently suffer from accumulated learning deficits, motivational declines, and prerequisite knowledge gaps that are challenging to remediate within the remaining term. 

Furthermore, educational data is multifaceted—encompassing study habits, parental education, domestic stability, peer socialization, and absenteeism. School administrators and educators lack automated, accessible tools to synthesize these disparate dimensions into proactive early-warning indicators.

---

## 2. Project Objectives

1. **Pipeline Engineering:** Construct an end-to-end, leak-free data processing and model training pipeline using Python 3.11+, Scikit-learn, and Pandas.
2. **Leakage Prevention:** Explicitly exclude period grades $G1$ and $G2$ from predictor inputs to guarantee that predictions reflect true pre-exam student attributes rather than duplicate interim marks.
3. **Rigorous Benchmarking:** Evaluate multiple linear and non-linear candidate models using 5-fold cross-validation and unbiased evaluation on held-out test data.
4. **Interactive Deployment:** Build a responsive, user-friendly Flask dashboard providing single-student inference, categorical academic tier mapping, and personalized remedial recommendations.
5. **Quality Assurance:** Implement a comprehensive automated testing suite covering unit transformations, inference edge cases, and HTTP route integrations.
6. **Ethical Transparency:** Articulate system limitations, demographic constraints, and non-punitive guidelines for responsible application in educational environments.

---

## 3. Literature & Background Overview

Educational Data Mining (EDM) and Learning Analytics (LA) have emerged as vital disciplines leveraging statistical learning to enhance pedagogical outcomes (Baker & Inventado, 2014). Early research by Cortez and Silva (2008) pioneered the use of data mining techniques on Portuguese secondary school cohorts, evaluating Decision Trees, Random Forests, Neural Networks, and Support Vector Machines.

A critical methodological consideration highlighted in EDM literature is **target leakage**. While incorporating first and second period grades ($G1$, $G2$) artificially inflates regression metrics ($R^2 > 0.80$), it converts the problem into an autoregressive grade-tracking exercise rather than an early-warning intervention model. When $G1$ and $G2$ are excluded, the machine learning task shifts to identifying structural and behavioral impediments to learning—such as excessive alcohol consumption, high absenteeism, lack of home internet, or insufficient parental schooling.

---

## 4. Methodology & Machine Learning Pipeline

### 4.1 Dataset Characteristics
The system leverages the UC Irvine Machine Learning Repository's **Student Performance Data Set** (*student-mat.csv*), recording math course records from two Portuguese public secondary schools:
- **Sample Size:** 395 student instances.
- **Attributes:** 33 total attributes (30 predictor features, 2 intermediate period grades, 1 final target).
- **Target Variable ($G3$):** Integer grade ranging from 0 to 20 points, where $\ge 10$ designates a passing mark.

### 4.2 Feature Categorization
- **13 Numeric Features:** `age`, `Medu`, `Fedu`, `traveltime`, `studytime`, `failures`, `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health`, `absences`.
- **17 Categorical Features:** `school`, `sex`, `address`, `famsize`, `Pstatus`, `Mjob`, `Fjob`, `reason`, `guardian`, `schoolsup`, `famsup`, `paid`, `activities`, `nursery`, `higher`, `internet`, `romantic`.

### 4.3 Preprocessing & Partitioning
1. **Train/Test Partition:** Partitioned into 80% training ($n=316$) and 20% testing ($n=79$) using a fixed random seed (`random_state=42`).
2. **ColumnTransformer Construction:**
   - `StandardScaler`: Applied to all numeric continuous and ordinal indicators to ensure zero mean and unit variance.
   - `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`: Encodes categorical variables into binary indicator vectors.
3. **Pipeline Encapsulation:** The preprocessor and regressor are fused into an immutable scikit-learn `Pipeline`, preventing data leakage during cross-validation and inference.

---

## 5. System Requirements & Technology Stack

### System Requirements
- **Operating System:** Windows 10 / 11 (64-bit)
- **Runtime:** Python 3.11 or 3.12
- **Memory:** Minimum 4 GB RAM
- **Disk Space:** ~500 MB (including virtual environment and dependencies)

### Technology Stack
- **Data Manipulation & Computation:** Pandas 3.0+, NumPy 2.4+
- **Machine Learning & Pipeline:** Scikit-learn 1.9+, Joblib 1.5+
- **Visualization:** Matplotlib 3.11+, Seaborn 0.13+, Chart.js 4.4+
- **Web Backend & Routing:** Flask 3.1+, Jinja2 3.1+
- **Frontend Architecture:** HTML5, Modern Vanilla CSS3, JavaScript
- **Test Automation:** Pytest 9.1+
- **Notebook & Research:** Jupyter, Nbformat, Nbclient, Ipykernel

---

## 6. Experimental Results & Model Selection

### 6.1 5-Fold Cross-Validation & Held-Out Test Evaluation

All candidates were cross-validated on the 316 training samples. Test results were generated exclusively from the held-out 79 test samples:

| Candidate Model | 5-Fold CV MAE | 5-Fold CV R² | Test MAE | Test RMSE | Test R² |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline Regressor (Mean)** | 3.403 | -0.035 | 3.646 | 4.550 | -0.010 |
| **Linear Regression (OLS)** | 3.523 | -0.092 | 3.395 | 4.196 | 0.141 |
| **Ridge Regression ($\alpha=10.0$)** | 3.417 | -0.016 | 3.374 | 4.180 | 0.148 |
| **Random Forest Regressor** | **2.971** | **0.208** | **3.173** | **3.949** | **0.239** |
| **Gradient Boosting Regressor** | 3.052 | 0.198 | 3.171 | 3.929 | 0.247 |

### 6.2 Key Findings
1. **Random Forest Superiority:** Random Forest achieved the lowest cross-validation MAE (2.971), successfully modeling non-linear interactions among features (e.g., interaction between study time and parental education).
2. **Feature Importance Insights:** Analysis of Gini feature importances revealed that the top predictors of final academic performance are:
   - Past academic failures (`failures`)
   - School absences (`absences`)
   - Student age (`age`)
   - Mother's and father's educational attainment (`Medu`, `Fedu`)
   - Weekend alcohol consumption (`Walc`) and going out frequency (`goout`)
3. **Generalization Stability:** The test set MAE (3.173) was closely aligned with the cross-validation MAE (2.971), indicating healthy regularization without overfitting.

---

## 7. Software Architecture & Implementation

### 7.1 Backend Modularization
- `src/data_loader.py`: Handles CSV parsing, schema enforcement, duplicate elimination, missing value imputation, and descriptive aggregation.
- `src/preprocessing.py`: Implements `ColumnTransformer` builder and strict server-side dictionary validation (`validate_student_input`).
- `src/train_model.py`: Automates candidate training, 5-fold CV, model serialization (`models/student_model.joblib`), and plot generation.
- `src/evaluate_model.py`: Generates metric payloads and diagnostic visualizations (model comparison, residual distribution, feature importance).
- `src/predict.py`: Manages model loading, numeric prediction, performance tier mapping, and heuristic recommendation rules.
- `app.py`: Exposes web routes (`/`, `/predict`, `/analytics`, `/evaluation`, `/about`) and REST endpoints (`/api/predict`, `/api/stats`).

### 7.2 Web User Interface
The UI implements an academic, data-centric design system:
- High contrast, dark navy navigation sidebar (`#0f172a`).
- Accessible, clean light canvas with card hierarchy and status badges.
- Dynamic responsive charts powered by Chart.js.
- Instant form bounds feedback and reset functionality.

### 7.3 Automated Testing
The project includes a 21-test Pytest test suite (`tests/`):
- `test_preprocessing.py`: Data ingestion, leakage exclusion, and schema validation.
- `test_prediction.py`: Pipeline loading, inference range verification, and edge case responses.
- `test_routes.py`: HTTP status codes, form submissions, REST JSON endpoints, and custom error handlers.
- **Pass Rate:** 21 / 21 passed (100%).

---

## 8. Limitations & Ethical Considerations

1. **Non-Deterministic Guidance:** Statistical predictions provide probabilistic risk indicators, not definitive appraisals of individual human potential. They must never be used for punitive sorting or tracking.
2. **Geographic & Cultural Scope:** Data was gathered from Portuguese secondary schools in 2005–2006. Models deployed in disparate educational contexts must be calibrated on local student populations.
3. **Data Privacy:** To respect student confidentiality, the web application does not persist submitted records to a permanent database; all inferences are executed transiently in memory.

---

## 9. Conclusion

The AI-Based Student Performance Prediction System establishes a robust, reproducible, and leak-free machine learning workflow for educational analytics. By discarding interim period grades, the model successfully identifies authentic pre-assessment risk factors, outperforming naive baselines and linear algorithms. Delivered through an intuitive web interface with automated testing and thorough documentation, the system demonstrates how responsible artificial intelligence can empower educators with proactive, actionable academic guidance.

---

## 10. References

1. Cortez, P., & Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance*. In Proceedings of the 5th Annual Future Business Technology Conference (FUBUTEC 2008), pp. 5–12, Porto, Portugal. EUROSIS-ETI. ISBN 978-9077381-39-7.
2. Baker, R. S., & Inventado, P. S. (2014). *Educational Data Mining and Learning Analytics*. In Learning Analytics (pp. 61-75). Springer, New York, NY.
3. Romero, C., & Ventura, S. (2010). *Educational Data Mining: A Review of the State of the Art*. IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews), 40(6), 601–618.
4. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825–2830.
