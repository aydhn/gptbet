import pandas as pd
import pytest

from sports_signal_bot.features.builders.market_odds import MarketOddsFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


def test_market_odds_feature_builder_null_safe():
    builder = MarketOddsFeatureBuilder()
    context = FeatureBuildContext(sport="football", run_id="test")

    events_df = pd.DataFrame({"event_id": ["e1"]})
    df = builder.build(context, {"events": events_df})  # No odds data

    assert "event_id" in df.columns
    assert "favorite_implied_prob" in df.columns
    assert df["favorite_implied_prob"].isnull().all()


def test_market_odds_feature_builder_with_data():
    builder = MarketOddsFeatureBuilder()
    context = FeatureBuildContext(sport="football", run_id="test")

    events_df = pd.DataFrame(
        {"event_id": ["e1"], "event_datetime_utc": ["2023-01-02T10:00:00Z"]}
    )
    odds_df = pd.DataFrame(
        {"event_id": ["e1"], "snapshot_time_utc": ["2023-01-01T10:00:00Z"]}
    )

    df = builder.build(context, {"events": events_df, "odds": odds_df})

    assert "event_id" in df.columns
    assert "favorite_implied_prob" in df.columns
