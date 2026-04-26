import pytest
from sports_signal_bot.sizing.contracts import SizingConfig, StakeSizingInputRecord
from sports_signal_bot.sizing.runner import SizingRunner

def test_fractional_kelly_strategy_flow():
    config = SizingConfig(
        default_sizing_strategy="fractional_kelly",
        fractional_kelly_default=0.25, # 1/4 Kelly
        max_fraction_per_decision=1.0,
        action_class_fraction_caps={}
    )
    runner = SizingRunner(config)

    rec = StakeSizingInputRecord(
        event_id="e1", sport="test", market_type="1x2", action_class="approved", selected_side="home",
        final_selection_probability=0.55, market_odds=2.0, implied_probability=0.5,
        edge_estimate=0.05, confidence_score=1.0, current_bankroll=1000
    )

    decision = runner.process_decision(rec)

    # Kelly = 0.1
    # Quarter Kelly = 0.025
    assert decision.kelly_fraction_raw == pytest.approx(0.1)
    assert decision.final_stake_fraction == pytest.approx(0.025)
    assert decision.final_stake_units == pytest.approx(25.0)

def test_capped_kelly_strategy_flow():
    config = SizingConfig(
        default_sizing_strategy="capped_fractional_kelly",
        fractional_kelly_default=0.5, # Half Kelly
        max_fraction_per_decision=0.04, # Hard global cap at 4%
        action_class_fraction_caps={}
    )
    runner = SizingRunner(config)

    rec = StakeSizingInputRecord(
        event_id="e1", sport="test", market_type="1x2", action_class="approved", selected_side="home",
        final_selection_probability=0.55, market_odds=2.0, implied_probability=0.5,
        edge_estimate=0.05, confidence_score=1.0, current_bankroll=1000
    )

    decision = runner.process_decision(rec)

    # Kelly = 0.1
    # Half Kelly = 0.05 -> Should be capped at 0.04
    assert decision.kelly_fraction_raw == pytest.approx(0.1)
    assert decision.final_stake_fraction == pytest.approx(0.04)
    assert len(decision.caps_applied) > 0
