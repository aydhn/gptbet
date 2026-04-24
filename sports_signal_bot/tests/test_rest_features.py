import pytest
import pandas as pd
from sports_signal_bot.features.builders.rest import RestFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext

def test_rest_feature_builder():
    builder = RestFeatureBuilder()
    context = FeatureBuildContext(sport="football", run_id="test")

    events_df = pd.DataFrame({
        "event_id": ["e1"],
        "event_datetime_utc": ["2023-01-01T10:00:00Z"]
    })

    df = builder.build(context, {"events": events_df})

    assert "event_id" in df.columns
    assert "home_days_since_last_match" in df.columns
    assert df["home_days_since_last_match"].iloc[0] == 7.0
