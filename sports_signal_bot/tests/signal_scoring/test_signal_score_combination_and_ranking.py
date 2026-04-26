from sports_signal_bot.signal_scoring.contracts import SignalComponentRecord, SignalScoreRecord, SignalStatus
from sports_signal_bot.signal_scoring.combine import combine_signal_components, normalize_signal_score
from sports_signal_bot.signal_scoring.ranking import rank_signals

def test_combine_signal_components():
    comps = SignalComponentRecord(
        edge_estimate=0.1,
        confidence_score=0.5,
        uncertainty_penalty=0.1,
        disagreement_penalty=0.2,
        data_quality_penalty=0.0,
        source_health_penalty=0.0,
        regime_adjustment=0.05
    )
    weights = {
        "edge_weight": 2.0, "confidence_weight": 1.0, "uncertainty_penalty_weight": 1.0,
        "disagreement_penalty_weight": 1.0, "data_quality_penalty_weight": 1.0,
        "source_health_penalty_weight": 1.0, "regime_adjustment_weight": 1.0
    }
    assert round(combine_signal_components(comps, weights), 2) == 0.45

def test_normalize_signal_score():
    assert normalize_signal_score(0.5, min_expected=0.0, max_expected=1.0) == 50.0
    assert normalize_signal_score(-0.5, min_expected=-1.0, max_expected=1.0) == 25.0
    assert normalize_signal_score(1.5, min_expected=0.0, max_expected=1.0) == 100.0

def test_rank_signals():
    s1 = SignalScoreRecord(
        event_id="e1", sport="football", market_type="1x2", selection="home",
        final_probability=0.6, components=SignalComponentRecord(),
        final_signal_score=0.8, strategy_name="test", status=SignalStatus.SCORED
    )
    s2 = SignalScoreRecord(
        event_id="e2", sport="football", market_type="1x2", selection="home",
        final_probability=0.6, components=SignalComponentRecord(),
        final_signal_score=0.9, strategy_name="test", status=SignalStatus.SCORED
    )
    s3 = SignalScoreRecord(
        event_id="e3", sport="football", market_type="1x2", selection="home",
        final_probability=0.6, components=SignalComponentRecord(),
        final_signal_score=0.7, strategy_name="test", status=SignalStatus.WEAK_SIGNAL
    )

    ranked = rank_signals([s1, s2, s3])

    assert len(ranked) == 3
    assert ranked[0].event_id == "e2"
    assert ranked[0].rank == 1
    assert ranked[0].tier == "S"

    assert ranked[1].event_id == "e1"
    assert ranked[1].rank == 2
    assert ranked[1].tier == "S"

    assert ranked[2].event_id == "e3"
    assert ranked[2].rank == 3
    assert ranked[2].tier == "C"
