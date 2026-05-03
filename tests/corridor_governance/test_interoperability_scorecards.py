import pytest
from sports_signal_bot.corridor_governance.scorecards import compute_scorecard_dimensions, map_score_to_band
from sports_signal_bot.corridor_governance.penalties import apply_scorecard_penalties
from sports_signal_bot.corridor_governance.contracts import SovereignInteroperabilityScorecardRecord

def test_compute_scorecard_dimensions():
    data = {"corridor_freshness": 50, "treaty_freshness": 40}
    weights = {"corridor_freshness": 1.0, "treaty_freshness": 1.5}
    computed = compute_scorecard_dimensions(data, weights)
    assert computed["corridor_freshness"] == 50.0
    assert computed["treaty_freshness"] == 60.0

def test_map_score_to_band():
    assert map_score_to_band(95) == "high_confidence_interop"
    assert map_score_to_band(80) == "strong"
    assert map_score_to_band(65) == "workable"
    assert map_score_to_band(45) == "guarded"
    assert map_score_to_band(25) == "weak"
    assert map_score_to_band(10) == "very_weak"

def test_apply_scorecard_penalties():
    sc = SovereignInteroperabilityScorecardRecord(
        scorecard_id="s1", scored_scope="s", scored_corridor_refs=[], scored_treaty_refs=[],
        region_pair_ref="rp", dimension_scores={}, overall_score=85.0, overall_band="strong",
        caveat_summary=[], blocking_gaps=[], warnings=[]
    )
    sc = apply_scorecard_penalties(sc, 20.0)
    assert sc.overall_score == 65.0
    assert sc.overall_band == "workable"
