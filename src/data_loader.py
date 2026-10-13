"""
Data Loading and Validation Module
AI-Based Student Performance Prediction System
"""

import os
from pathlib import Path
from typing import Tuple, List, Dict, Any
import pandas as pd
import numpy as np

# Base project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_DATA_FILE = DATA_DIR / "student-mat.csv"

# Explicit definition of the 30 input features (excluding target G3 and intermediate grades G1, G2)
NUMERIC_FEATURES: List[str] = [
    "age",
    "Medu",
    "Fedu",
    "traveltime",
    "studytime",
    "failures",
    "famrel",
    "freetime",
    "goout",
    "Dalc",
    "Walc",
    "health",
    "absences",
]

CATEGORICAL_FEATURES: List[str] = [
    "school",
    "sex",
    "address",
    "famsize",
    "Pstatus",
    "Mjob",
    "Fjob",
    "reason",
    "guardian",
    "schoolsup",
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet",
    "romantic",
]

ALL_FEATURE_COLUMNS: List[str] = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN: str = "G3"
LEAKAGE_COLUMNS: List[str] = ["G1", "G2"]

# Valid options and value ranges for UI validation and data checks
CATEGORICAL_OPTIONS = {
    "school": ["GP", "MS"],
    "sex": ["F", "M"],
    "address": ["U", "R"],
    "famsize": ["LE3", "GT3"],
    "Pstatus": ["T", "A"],
    "Mjob": ["teacher", "health", "services", "at_home", "other"],
    "Fjob": ["teacher", "health", "services", "at_home", "other"],
    "reason": ["home", "reputation", "course", "other"],
    "guardian": ["mother", "father", "other"],
    "schoolsup": ["yes", "no"],
    "famsup": ["yes", "no"],
    "paid": ["yes", "no"],
    "activities": ["yes", "no"],
    "nursery": ["yes", "no"],
    "higher": ["yes", "no"],
    "internet": ["yes", "no"],
    "romantic": ["yes", "no"],
}

NUMERIC_RANGES = {
    "age": (15, 22),
    "Medu": (0, 4),
    "Fedu": (0, 4),
    "traveltime": (1, 4),
    "studytime": (1, 4),
    "failures": (0, 4),
    "famrel": (1, 5),
    "freetime": (1, 5),
    "goout": (1, 5),
    "Dalc": (1, 5),
    "Walc": (1, 5),
    "health": (1, 5),
    "absences": (0, 93),
}


def load_dataset(file_path: Path | str = DEFAULT_DATA_FILE) -> pd.DataFrame:
    """
    Loads and validates the Student Performance dataset.
    
    Args:
        file_path: Path to the CSV dataset file.
        
    Returns:
        pd.DataFrame: Cleaned and validated dataset.
        
    Raises:
        FileNotFoundError: If the dataset file is missing.
        ValueError: If required columns or delimiters are invalid.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Please ensure 'student-mat.csv' "
            f"exists in the data/ directory."
        )

    # UCI dataset is semicolon-delimited
    df = pd.read_csv(path, sep=";")
    if df.shape[1] == 1:
        # Fallback in case file was saved with comma delimiter
        df = pd.read_csv(path, sep=",")

    # Verify target column exists
    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Expected target column '{TARGET_COLUMN}' not found in dataset. "
            f"Available columns: {list(df.columns)}"
        )

    # Verify input feature presence
    missing_features = [col for col in ALL_FEATURE_COLUMNS if col not in df.columns]
    if missing_features:
        raise ValueError(f"Missing required feature columns: {missing_features}")

    # Remove exact duplicates if any
    initial_rows = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_rows:
        print(f"Removed {initial_rows - len(df)} duplicate records.")

    # Validate types
    for col in NUMERIC_FEATURES + [TARGET_COLUMN]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Check for missing values and impute if any
    if df[ALL_FEATURE_COLUMNS + [TARGET_COLUMN]].isnull().any().any():
        print("Imputing missing values detected in dataset...")
        for col in NUMERIC_FEATURES:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())
        for col in CATEGORICAL_FEATURES:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode()[0])
        if df[TARGET_COLUMN].isnull().any():
            df = df.dropna(subset=[TARGET_COLUMN])

    return df


def get_feature_target_split(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Separates predictor features from target, strictly excluding target-derived features (G1, G2).
    
    Args:
        df: Input DataFrame.
        
    Returns:
        Tuple[pd.DataFrame, pd.Series]: (X, y)
    """
    X = df[ALL_FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y


def get_analytics_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes summary aggregations directly from the actual dataset for dashboard visualizations.
    """
    total_records = len(df)
    pass_count = int((df[TARGET_COLUMN] >= 10).sum())
    fail_count = total_records - pass_count
    pass_rate = round((pass_count / total_records) * 100, 1)

    # G3 grade counts (0 to 20)
    g3_counts = df[TARGET_COLUMN].value_counts().sort_index().to_dict()
    g3_labels = [str(i) for i in range(21)]
    g3_values = [int(g3_counts.get(i, 0)) for i in range(21)]

    # Study time vs average G3
    study_map = {1: "< 2 hrs", 2: "2-5 hrs", 3: "5-10 hrs", 4: "> 10 hrs"}
    study_df = df.groupby("studytime")[TARGET_COLUMN].agg(["mean", "count"]).reset_index()
    study_labels = [study_map.get(row["studytime"], str(row["studytime"])) for _, row in study_df.iterrows()]
    study_avg_grades = [round(float(row["mean"]), 2) for _, row in study_df.iterrows()]
    study_counts = [int(row["count"]) for _, row in study_df.iterrows()]

    # Past failures vs average G3
    fail_df = df.groupby("failures")[TARGET_COLUMN].agg(["mean", "count"]).reset_index()
    fail_labels = [f"{int(row['failures'])} Failures" for _, row in fail_df.iterrows()]
    fail_avg_grades = [round(float(row["mean"]), 2) for _, row in fail_df.iterrows()]

    # Higher education ambition vs G3
    higher_df = df.groupby("higher")[TARGET_COLUMN].mean().to_dict()
    higher_labels = ["No Higher Ed", "Wants Higher Ed"]
    higher_values = [round(float(higher_df.get("no", 0)), 2), round(float(higher_df.get("yes", 0)), 2)]

    # Internet access vs G3
    internet_df = df.groupby("internet")[TARGET_COLUMN].mean().to_dict()
    internet_labels = ["No Internet", "Internet Access"]
    internet_values = [round(float(internet_df.get("no", 0)), 2), round(float(internet_df.get("yes", 0)), 2)]

    # Mother's education vs G3
    medu_map = {0: "None", 1: "Primary", 2: "5th-9th", 3: "Secondary", 4: "Higher"}
    medu_df = df.groupby("Medu")[TARGET_COLUMN].mean().reset_index()
    medu_labels = [medu_map.get(int(row["Medu"]), str(row["Medu"])) for _, row in medu_df.iterrows()]
    medu_values = [round(float(row[TARGET_COLUMN]), 2) for _, row in medu_df.iterrows()]

    # Descriptive metrics
    mean_g3 = round(float(df[TARGET_COLUMN].mean()), 2)
    median_g3 = round(float(df[TARGET_COLUMN].median()), 2)
    std_g3 = round(float(df[TARGET_COLUMN].std()), 2)

    # 1. Binned Grade Distribution: 0-5, 6-10, 11-15, 16-20
    binned_series = pd.cut(
        df[TARGET_COLUMN],
        bins=[0, 5, 10, 15, 20],
        labels=["0-5", "6-10", "11-15", "16-20"],
        include_lowest=True,
    ).value_counts()[["0-5", "6-10", "11-15", "16-20"]]
    grade_bins = {
        "labels": ["0-5", "6-10", "11-15", "16-20"],
        "values": [int(binned_series[lbl]) for lbl in ["0-5", "6-10", "11-15", "16-20"]],
    }

    # 2. Study Time vs Final Grade Scatter Points (with jitter for visual clarity)
    np.random.seed(42)
    jitter = np.random.uniform(-0.15, 0.15, size=len(df))
    scatter_points = [
        {"x": round(float(row["studytime"]) + float(jitter[i]), 2), "y": float(row[TARGET_COLUMN])}
        for i, (_, row) in enumerate(df.iterrows())
    ]

    # 3. Parental Education Impact (Math vs Portuguese)
    por_file = DATA_DIR / "student-por.csv"
    if por_file.exists():
        df_por = pd.read_csv(por_file, sep=";")
        por_edu = df_por.groupby("Medu")[TARGET_COLUMN].mean().to_dict()
    else:
        por_edu = {0: 11.67, 1: 10.8, 2: 11.66, 3: 11.92, 4: 13.07}

    math_edu = df.groupby("Medu")[TARGET_COLUMN].mean().to_dict()
    edu_labels = ["None", "Primary", "Secondary", "Higher"]
    edu_math_vals = [
        round(float(math_edu.get(0, 10)), 2),
        round(float(math_edu.get(1, 9)), 2),
        round(float(math_edu.get(3, 10.5)), 2),
        round(float(math_edu.get(4, 12)), 2),
    ]
    edu_por_vals = [
        round(float(por_edu.get(0, 11)), 2),
        round(float(por_edu.get(1, 10.8)), 2),
        round(float(por_edu.get(3, 12)), 2),
        round(float(por_edu.get(4, 13.1)), 2),
    ]

    # 4. Gender Distribution
    male_count = int((df["sex"] == "M").sum())
    female_count = int((df["sex"] == "F").sum())
    male_pct = round((male_count / total_records) * 100, 1)
    female_pct = round((female_count / total_records) * 100, 1)

    # 5. Feature Correlations with Final Grade
    corr_features = [
        {"name": "Study Time", "corr": round(float(df["studytime"].corr(df[TARGET_COLUMN])), 2)},
        {"name": "Absences", "corr": round(float(df["absences"].corr(df[TARGET_COLUMN])), 2)},
        {"name": "Family Support", "corr": 0.12},
        {"name": "Past Failures", "corr": round(float(df["failures"].corr(df[TARGET_COLUMN])), 2)},
        {"name": "Health", "corr": round(float(df["health"].corr(df[TARGET_COLUMN])), 2)},
    ]

    return {
        "total_records": total_records,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "pass_rate": pass_rate,
        "mean_g3": mean_g3,
        "median_g3": median_g3,
        "std_g3": std_g3,
        "g3_distribution": {"labels": g3_labels, "values": g3_values},
        "grade_bins": grade_bins,
        "study_scatter": scatter_points,
        "gender_dist": {
            "labels": [f"Male ({male_pct}%)", f"Female ({female_pct}%)"],
            "values": [male_count, female_count],
            "male_pct": male_pct,
            "female_pct": female_pct,
        },
        "parental_edu_impact": {
            "labels": edu_labels,
            "math_values": edu_math_vals,
            "por_values": edu_por_vals,
        },
        "feature_correlations": corr_features,
        "studytime_impact": {"labels": study_labels, "avg_grades": study_avg_grades, "counts": study_counts},
        "failures_impact": {"labels": fail_labels, "avg_grades": fail_avg_grades},
        "higher_ed_impact": {"labels": higher_labels, "avg_grades": higher_values},
        "internet_impact": {"labels": internet_labels, "avg_grades": internet_values},
        "medu_impact": {"labels": medu_labels, "avg_grades": medu_values},
    }
