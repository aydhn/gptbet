import pytest
from sports_signal_bot.sizing.adjustments import compute_sizing_adjustments
from sports_signal_bot.sizing.contracts import StakeSizingInputRecord, SizingConfig

def test_compute_adjustments():
    config = SizingConfig(
        confidence_multiplier_bounds=(0.5, 1.5),
        uncertainty_penalty_bounds=(0.0, 0.5)
    )

    # Base case (perfect conditions)
    rec_good = StakeSizingInputRecord(
        event_id="e1", sport="test", market_type="1x2", action_class="A", selected_side="home",
        final_selection_probability=0.55, market_odds=2.0, implied_probability=0.5,
        edge_estimate=0.05, confidence_score=1.0, current_bankroll=1000
    )
    adj = compute_sizing_adjustments(rec_good, config)
    assert adj.combined_multiplier == pytest.approx(1.0)

    # Low confidence case
    rec_low_conf = StakeSizingInputRecord(
        event_id="e1", sport="test", market_type="1x2", action_class="A", selected_side="home",
        final_selection_probability=0.55, market_odds=2.0, implied_probability=0.5,
        edge_estimate=0.05, confidence_score=0.5, current_bankroll=1000
    )
    adj = compute_sizing_adjustments(rec_low_conf, config)
    # Score 0.5 -> mapped to bounds (0.5 to 1.5). Midpoint is ~0.75
    assert adj.confidence_multiplier == pytest.approx(0.75)

    # High uncertainty case
    rec_uncert = StakeSizingInputRecord(
        event_id="e1", sport="test", market_type="1x2", action_class="A", selected_side="home",
        final_selection_probability=0.55, market_odds=2.0, implied_probability=0.5,
        edge_estimate=0.05, confidence_score=1.0, current_bankroll=1000,
        uncertainty_penalty=0.2 # 20% dampening
    )
    adj = compute_sizing_adjustments(rec_uncert, config)
    assert adj.uncertainty_multiplier == pytest.approx(0.8)
