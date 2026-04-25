import pandas as pd
import pytest

from sports_signal_bot.features.builders.rolling_form import \
    RollingFormFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


def test_rolling_form_builder():
    builder = RollingFormFeatureBuilder()
    context = FeatureBuildContext(sport="football", run_id="test")

    events_df = pd.DataFrame({"event_id": ["e1"]})
    df = builder.build(context, {"events": events_df})

    assert "event_id" in df.columns
    assert "home_last_5_wins_proxy" in df.columns
    assert not df.empty
