import pytest

from sports_signal_bot.regimes.factory import RegimeFactory
from sports_signal_bot.regimes.inputs import build_event_regime_inputs
from sports_signal_bot.regimes.runner import RegimeRunner
from sports_signal_bot.regimes.thresholds import (RegimeConfig,
                                                  RegimeThresholdsConfig)


def test_multi_axis_assignment():
    t_config = RegimeThresholdsConfig()
    r_config = RegimeConfig(enabled_regime_families=["form", "schedule"])
    factory = RegimeFactory(t_config, r_config)
    runner = RegimeRunner(factory)

    inputs = build_event_regime_inputs(
        event_id="1",
        sport="f",
        market_type="1x2",
        features={
            "home_form_score": 0.8,
            "away_form_score": 0.8,
            "home_rest_days": 2,
            "away_rest_days": 2,
        },
    )

    res = runner.assign_event_regimes(inputs)
    assert len(res.event_regimes) == 2
    families = [r.regime_family for r in res.event_regimes]
    assert "form" in families
    assert "schedule" in families
