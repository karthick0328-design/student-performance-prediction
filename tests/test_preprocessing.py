"""
Unit tests for data loading and preprocessing.
"""

import pytest
import pandas as pd
from pathlib import Path

from src.data_loader import (
    load_dataset,
    get_feature_target_split,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    ALL_FEATURE_COLUMNS,
    TARGET_COLUMN,
    LEAKAGE_COLUMNS,
)
from src.preprocessing import build_preprocessor, validate_student_input


def test_dataset_loading_and_shape():
    """Verify raw dataset loads correctly with expected column count."""
    df = load_dataset()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 395
    assert TARGET_COLUMN in df.columns
    for col in ALL_FEATURE_COLUMNS:
        assert col in df.columns


def test_leakage_exclusion():
    """Verify target and intermediate period grades (G1, G2) are strictly excluded from X."""
    df = load_dataset()
    X, y = get_feature_target_split(df)
    assert X.shape[1] == 30
    assert len(y) == len(df)
    for col in LEAKAGE_COLUMNS + [TARGET_COLUMN]:
        assert col not in X.columns


def test_preprocessor_pipeline_transformation():
    """Verify ColumnTransformer scales numerics and one-hot encodes categoricals."""
    df = load_dataset()
    X, _ = get_feature_target_split(df)
    preprocessor = build_preprocessor()
    transformed = preprocessor.fit_transform(X)
    assert transformed.shape[0] == len(df)
    # 13 numeric columns + one-hot encoded categoricals
    assert transformed.shape[1] > 30


def test_validate_student_input_valid():
    """Verify valid input passes validation cleanly."""
    valid_data = {
        "school": "GP", "sex": "F", "age": 17, "address": "U", "famsize": "GT3",
        "Pstatus": "T", "Medu": 3, "Fedu": 3, "Mjob": "services", "Fjob": "services",
        "reason": "course", "guardian": "mother", "traveltime": 1, "studytime": 2,
        "failures": 0, "schoolsup": "no", "famsup": "yes", "paid": "no",
        "activities": "yes", "nursery": "yes", "higher": "yes", "internet": "yes",
        "romantic": "no", "famrel": 4, "freetime": 3, "goout": 3, "Dalc": 1,
        "Walc": 2, "health": 4, "absences": 4,
    }
    df_clean, errors = validate_student_input(valid_data)
    assert len(errors) == 0
    assert df_clean.shape == (1, 30)


def test_validate_student_input_invalid_values():
    """Verify out-of-range numeric values and illegal categories are rejected."""
    invalid_data = {
        "school": "INVALID_SCHOOL",  # Invalid
        "sex": "F", "age": 99,       # Out of range (15-22)
        "address": "U", "famsize": "GT3", "Pstatus": "T", "Medu": 3, "Fedu": 3,
        "Mjob": "services", "Fjob": "services", "reason": "course", "guardian": "mother",
        "traveltime": 1, "studytime": 2, "failures": 0, "schoolsup": "no", "famsup": "yes",
        "paid": "no", "activities": "yes", "nursery": "yes", "higher": "yes",
        "internet": "yes", "romantic": "no", "famrel": 4, "freetime": 3, "goout": 3,
        "Dalc": 1, "Walc": 2, "health": 4, "absences": 4,
    }
    df_clean, errors = validate_student_input(invalid_data)
    assert "school" in errors
    assert "age" in errors
    assert df_clean.empty


def test_validate_student_input_missing_field():
    """Verify missing field is detected."""
    incomplete_data = {"school": "GP", "sex": "F"}
    df_clean, errors = validate_student_input(incomplete_data)
    assert len(errors) > 0
    assert "studytime" in errors
