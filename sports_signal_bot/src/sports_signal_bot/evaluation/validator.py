from typing import List

import pandas as pd


def validate_evaluation_data(df: pd.DataFrame, required_cols: List[str]) -> List[str]:
    """Validates dataframe before evaluation and returns warnings."""
    warnings = []

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Evaluation data missing required columns: {missing_cols}")

    if "true_label" in df.columns:
        missing_labels = df["true_label"].isna().sum()
        if missing_labels > 0:
            warnings.append(
                f"Found {missing_labels} rows with missing true labels. They will be ignored."
            )

    if "predicted_class" in df.columns:
        missing_preds = df["predicted_class"].isna().sum()
        if missing_preds > 0:
            warnings.append(
                f"Found {missing_preds} rows with missing predicted classes."
            )

    return warnings


def filter_valid_evaluation_data(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows that cannot be evaluated (e.g. missing true label)."""
    if df.empty:
        return df

    if "true_label" in df.columns:
        df = df.dropna(subset=["true_label"])

    if "prediction_status" in df.columns:
        df = df[df["prediction_status"] == "valid"]

    return df
