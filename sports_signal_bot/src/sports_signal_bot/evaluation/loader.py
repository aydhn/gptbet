from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


def load_evaluation_dataframe(
    file_paths: List[Path], required_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """Loads and concatenates prediction artifacts into a single DataFrame."""

    if not file_paths:
        return pd.DataFrame()

    dfs = []
    for path in file_paths:
        if path.suffix == ".csv":
            df = pd.read_csv(path)
        elif path.suffix in [".parquet"]:
            df = pd.read_parquet(path)
        elif path.suffix in [".json"]:
            df = pd.read_json(path, orient="records")
        else:
            raise ValueError(f"Unsupported file format for evaluation: {path}")

        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    if required_cols:
        missing = [c for c in required_cols if c not in combined_df.columns]
        if missing:
            raise ValueError(f"Missing required columns in loaded data: {missing}")

    return combined_df


def extract_probability_columns(df: pd.DataFrame, class_labels: List[str]) -> List[str]:
    """Helper to find or construct probability column names based on class labels."""
    # Try exact match first
    prob_cols = [f"prob_{label}" for label in class_labels]

    if all(c in df.columns for c in prob_cols):
        return prob_cols

    # If not found, try to find columns that look like probabilities
    # This is a naive fallback, actual implementation depends on how predictions are saved
    available_cols = df.columns.tolist()
    found_cols = [c for c in available_cols if c.startswith("prob_")]

    if len(found_cols) == len(class_labels):
        return sorted(found_cols)

    return []
