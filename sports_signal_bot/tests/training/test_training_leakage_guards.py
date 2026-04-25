import pandas as pd
import pytest

from sports_signal_bot.core.exceptions import LeakageDetectedError
from sports_signal_bot.training.leakage import (
    audit_feature_target_alignment, detect_suspicious_feature_columns,
    enforce_pre_match_only_feature_policy)


def test_detect_suspicious_columns():
    cols = [
        "home_rating",
        "away_rating",
        "final_score_home",
        "target_variable",
        "weather",
    ]
    suspicious = detect_suspicious_feature_columns(cols)
    assert "final_score_home" in suspicious
    assert "target_variable" in suspicious
    assert "home_rating" not in suspicious
    assert "weather" not in suspicious


def test_audit_target_in_features():
    df = pd.DataFrame({"event_id": ["1"], "feat_1": [1.0], "actual_outcome": [1]})

    with pytest.raises(LeakageDetectedError):
        audit_feature_target_alignment(
            df, ["feat_1", "actual_outcome"], "actual_outcome"
        )


def test_enforce_temporal_ordering():
    df = pd.DataFrame(
        {
            "event_id": ["1", "2"],
            "event_datetime_utc": [pd.NaT, pd.Timestamp("2024-01-01")],
        }
    )

    with pytest.raises(ValueError):
        enforce_pre_match_only_feature_policy(df)
