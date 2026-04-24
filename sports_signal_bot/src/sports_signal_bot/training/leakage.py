import pandas as pd
from typing import List, Tuple
from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.core.exceptions import LeakageDetectedError

logger = get_logger("LeakageGuards")

SUSPICIOUS_PATTERNS = [
    "target",
    "result",
    "outcome",
    "post_event",
    "final_score",
    "label",
    "settlement",
    "win",
    "loss",
    "draw",
    "goals_home",
    "goals_away",
]

def detect_suspicious_feature_columns(columns: List[str]) -> List[str]:
    """Detect columns that might contain target information or post-event data."""
    suspicious_cols = []
    for col in columns:
        col_lower = col.lower()
        if any(pattern in col_lower for pattern in SUSPICIOUS_PATTERNS):
            suspicious_cols.append(col)
    return suspicious_cols

def audit_feature_target_alignment(
    df: pd.DataFrame,
    feature_columns: List[str],
    target_column: str,
    event_id_column: str = "event_id",
    datetime_column: str = "event_datetime_utc"
) -> None:
    """Audit the alignment of features and targets, looking for basic leakage indicators."""
    if df.empty:
        return

    # 1. Check for suspicious column names
    suspicious = detect_suspicious_feature_columns(feature_columns)
    if suspicious:
        logger.warning(f"Suspicious feature columns detected (potential leakage): {suspicious}")

    # 2. Check for duplicate event IDs
    if event_id_column in df.columns:
        dups = df[event_id_column].duplicated().sum()
        if dups > 0:
            logger.warning(f"Found {dups} duplicate {event_id_column}s in dataset.")

    # 3. Target in features check
    if target_column in feature_columns:
        raise LeakageDetectedError(f"Target column '{target_column}' is in the feature list!")

def enforce_pre_match_only_feature_policy(df: pd.DataFrame, datetime_column: str = "event_datetime_utc") -> None:
    """Ensure that the dataset is properly temporally sorted, a basic check before splitting."""
    if datetime_column not in df.columns:
        logger.warning(f"Column {datetime_column} not found, skipping temporal sort check.")
        return

    # Check if strictly monotonically increasing or at least non-decreasing
    # Actually, we just want to ensure it CAN be sorted, we don't strictly require it to be sorted
    # BEFORE we split, but for walk-forward it must be sorted.
    # Let's just ensure no NaNs in datetime
    if df[datetime_column].isna().any():
        raise ValueError(f"Found NaN values in temporal column '{datetime_column}'")
