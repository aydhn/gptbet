import pandas as pd
import pytest

from sports_signal_bot.features.builders.basketball_tempo import \
    BasketballTempoBuilder
from sports_signal_bot.features.builders.football_strength import \
    FootballTeamStrengthBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


def test_football_builder():
    builder = FootballTeamStrengthBuilder()
    context = FeatureBuildContext(sport="football", run_id="test")
    events_df = pd.DataFrame({"event_id": ["e1"]})
    df = builder.build(context, {"events": events_df})

    assert "home_rating_proxy" in df.columns
    assert df["home_rating_proxy"].iloc[0] == 1500.0


def test_basketball_builder():
    builder = BasketballTempoBuilder()
    context = FeatureBuildContext(sport="basketball", run_id="test")
    events_df = pd.DataFrame({"event_id": ["e1"]})
    df = builder.build(context, {"events": events_df})

    assert "home_pace_proxy" in df.columns
    assert df["home_pace_proxy"].iloc[0] == 100.0
