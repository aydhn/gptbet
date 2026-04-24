import pytest
import pandas as pd
from datetime import datetime
from sports_signal_bot.ratings.features import RatingFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext
from sports_signal_bot.ratings.contracts import RatingSnapshotRecord
from sports_signal_bot.core.constants import SportType

def test_rating_feature_builder():
    builder = RatingFeatureBuilder()
    ctx = FeatureBuildContext(sport="football", run_id="test")

    events_df = pd.DataFrame({
        "event_id": ["e1", "e2"],
        "home_team": ["A", "C"],
        "away_team": ["B", "D"]
    })

    snapshots = [
        RatingSnapshotRecord(
            event_id="e1", sport=SportType.FOOTBALL, league="L", season="S",
            event_datetime_utc=datetime.utcnow(), home_team_id="A", away_team_id="B",
            pre_home_rating=1550.0, pre_away_rating=1500.0,
            expected_home_score=0.6, expected_away_score=0.4
        )
    ]

    df = builder.build(ctx, {"events": events_df, "rating_snapshots": snapshots})

    assert len(df) == 2
    assert "rating_diff" in df.columns
    assert "rating_abs_diff" in df.columns

    # Event 1 features
    e1 = df.loc["e1"]
    assert e1["rating_home_pre"] == 1550.0
    assert e1["rating_diff"] == 50.0

    # Event 2 missing
    e2 = df.loc["e2"]
    assert pd.isna(e2["rating_home_pre"])

def test_rating_feature_builder_empty():
    builder = RatingFeatureBuilder()
    ctx = FeatureBuildContext(sport="football", run_id="test")
    events_df = pd.DataFrame({"event_id": ["e1"]})

    df = builder.build(ctx, {"events": events_df})
    assert len(df) == 1
    assert "rating_diff" in df.columns
    assert pd.isna(df.loc["e1", "rating_diff"])
