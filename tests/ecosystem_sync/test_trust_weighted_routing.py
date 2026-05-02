import pytest
from sports_signal_bot.ecosystem_sync.routing import EcosystemRoutingEngine
from sports_signal_bot.ecosystem_sync.contracts import RoutingCandidateRecord, RoutingScoreBreakdownRecord, RoutingPenaltyRecord

def test_compute_routing_score():
    engine = EcosystemRoutingEngine({
        "trust_weight_components": {
            "source_trust_weight_max": 40.0,
            "freshness_weight_max": 20.0,
            "capability_fit_weight_max": 15.0
        }
    })

    metadata = {"trust_ratio": 1.0, "freshness_ratio": 0.5, "capability_ratio": 1.0}
    breakdown = engine.compute_routing_weights(metadata)

    # 40*1.0 + 20*0.5 + 15*1.0 = 40 + 10 + 15 = 65
    assert breakdown.total_score == 65.0

    score = engine.compute_routing_score(breakdown, [RoutingPenaltyRecord(penalty_name="test", deduction=10.0)])
    assert score == 55.0

def test_rank_candidates():
    engine = EcosystemRoutingEngine({})
    c1 = RoutingCandidateRecord(candidate_ref="c1", score_breakdown=RoutingScoreBreakdownRecord(base_score=0, components=[], total_score=50), penalties=[])
    c2 = RoutingCandidateRecord(candidate_ref="c2", score_breakdown=RoutingScoreBreakdownRecord(base_score=0, components=[], total_score=80), penalties=[])

    ranked = engine.rank_routing_candidates([c1, c2])
    assert ranked[0].candidate_ref == "c2"
