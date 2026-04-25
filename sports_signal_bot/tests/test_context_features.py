import pandas as pd
import pytest

from sports_signal_bot.features.builders.context import ContextFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


def test_context_feature_builder():
    builder = ContextFeatureBuilder()
    context = FeatureBuildContext(sport="football", run_id="test")

    events_df = pd.DataFrame(
        {"event_id": ["e1"], "event_datetime_utc": ["2023-01-01T10:00:00Z"]}
    )

    df = builder.build(context, {"events": events_df})

    assert "event_id" in df.columns
    assert "sport" in df.columns
    assert df["sport"].iloc[0] == "football"
    assert "event_month" in df.columns
    assert df["event_month"].iloc[0] == 1
