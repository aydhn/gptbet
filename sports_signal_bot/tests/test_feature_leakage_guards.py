import pandas as pd
import pytest

from sports_signal_bot.features.utils.snapshots import select_feature_snapshot


def test_snapshot_leakage_guard():
    events_df = pd.DataFrame(
        {"event_id": ["e1"], "event_datetime_utc": ["2023-01-02T10:00:00Z"]}
    )

    odds_df = pd.DataFrame(
        {
            "event_id": ["e1", "e1"],
            "snapshot_time_utc": [
                "2023-01-01T10:00:00Z",
                "2023-01-03T10:00:00Z",
            ],  # one pre, one post
        }
    )

    safe_odds = select_feature_snapshot(events_df, odds_df, "strict_pre_match")

    assert len(safe_odds) == 1
