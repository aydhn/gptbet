import pytest

from sports_signal_bot.regimes.event.form import FormRegimeClassifier
from sports_signal_bot.regimes.event.market import \
    MarketDisagreementRegimeClassifier
from sports_signal_bot.regimes.inputs import build_event_regime_inputs
from sports_signal_bot.regimes.thresholds import RegimeThresholdsConfig


def test_form_regime_assignment():
    config = RegimeThresholdsConfig()
    classifier = FormRegimeClassifier(config)

    inputs = build_event_regime_inputs(
        event_id="1",
        sport="football",
        market_type="1x2",
        features={"home_form_score": 0.8, "away_form_score": 0.1},
    )
    records = classifier.assign_event_regimes(inputs)
    assert len(records) == 1
    assert records[0].regime_label == "mixed_form"
    assert records[0].regime_family == "form"


def test_market_disagreement_regime_assignment():
    config = RegimeThresholdsConfig()
    classifier = MarketDisagreementRegimeClassifier(config)

    # Simulate high disagreement
    inputs = build_event_regime_inputs(
        event_id="1",
        sport="football",
        market_type="1x2",
        source_probabilities={
            "s1": {"home": 0.8, "away": 0.2},
            "s2": {"home": 0.3, "away": 0.7},
        },
    )
    records = classifier.assign_event_regimes(inputs)
    assert any(r.regime_label == "high_source_disagreement" for r in records)
