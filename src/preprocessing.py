"""
Data Preprocessing and Pipeline Creation Module
AI-Based Student Performance Prediction System
"""

import sys
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.data_loader import (
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    ALL_FEATURE_COLUMNS,
    CATEGORICAL_OPTIONS,
    NUMERIC_RANGES,
)


def build_preprocessor() -> ColumnTransformer:
    """
    Constructs a ColumnTransformer that handles numeric scaling and categorical one-hot encoding.
    
    Returns:
        ColumnTransformer: Preprocessing pipeline.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                NUMERIC_FEATURES,
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )
    return preprocessor


def validate_student_input(data: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    Validates a single student record dictionary against expected features, types, and ranges.
    
    Args:
        data: Dictionary of input features.
        
    Returns:
        Tuple[pd.DataFrame, Dict[str, str]]: (Processed single-row DataFrame, error dictionary)
    """
    errors: Dict[str, str] = {}
    cleaned_record: Dict[str, Any] = {}

    # Check for missing keys
    for col in ALL_FEATURE_COLUMNS:
        if col not in data or data[col] is None or str(data[col]).strip() == "":
            errors[col] = f"Feature '{col}' is required."

    if errors:
        return pd.DataFrame(), errors

    # Validate numeric features
    for col in NUMERIC_FEATURES:
        val_str = str(data[col]).strip()
        try:
            val = float(val_str)
            min_val, max_val = NUMERIC_RANGES[col]
            if not (min_val <= val <= max_val):
                errors[col] = f"Must be between {min_val} and {max_val} (got {val})."
            else:
                cleaned_record[col] = val
        except ValueError:
            errors[col] = f"Must be a valid numeric number (got '{val_str}')."

    # Validate categorical features
    for col in CATEGORICAL_FEATURES:
        val_str = str(data[col]).strip()
        allowed = CATEGORICAL_OPTIONS[col]
        if val_str not in allowed:
            errors[col] = f"Must be one of: {', '.join(allowed)} (got '{val_str}')."
        else:
            cleaned_record[col] = val_str

    if errors:
        return pd.DataFrame(), errors

    # Return DataFrame with consistent column ordering
    df_clean = pd.DataFrame([cleaned_record])[ALL_FEATURE_COLUMNS]
    return df_clean, {}
