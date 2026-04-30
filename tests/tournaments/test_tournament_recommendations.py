import pytest
from src.sports_signal_bot.tournaments.contracts import TournamentCandidateRecord, TournamentRankingRecord, SafetyLane, RecommendationAction, ShortlistTier
from src.sports_signal_bot.simulation.contracts import RiskLevel
from src.sports_signal_bot.tournaments.recommendations import build_tournament_recommendation

def test_recommendation_building():
    c1 = TournamentCandidateRecord(
        candidate_id="c1", suggestion_id="s1", patch_id="p1", target_component_family="threshold",
        scope={}, risk_level=RiskLevel.LOW, support_strength=0.9, confidence_band="high",
        estimated_blast_radius=0.1, simulation_ref="ref1"
    )

    r1 = TournamentRankingRecord(
        candidate_id="c1", pareto_front=1, secondary_rank=1, lane=SafetyLane.SAFE_SHORTLIST_LANE,
        total_score=10.0, explanation="ok"
    )

    # Pareto Front 1 + Safe Lane + High Support = Approval
    rec = build_tournament_recommendation(c1, r1, SafetyLane.SAFE_SHORTLIST_LANE, merge_target_id=None)
    assert rec.tier == ShortlistTier.TIER_1_REVIEW_NOW
    assert rec.action == RecommendationAction.SHORTLIST_FOR_APPROVAL

    # Pareto Front 1 + Safe Lane + Low Support = Review
    c1.support_strength = 0.6
    rec = build_tournament_recommendation(c1, r1, SafetyLane.SAFE_SHORTLIST_LANE, merge_target_id=None)
    assert rec.action == RecommendationAction.SHORTLIST_FOR_REVIEW

    # Blocked Lane
    rec = build_tournament_recommendation(c1, r1, SafetyLane.BLOCKED_LANE, merge_target_id=None)
    assert rec.tier == ShortlistTier.TIER_4_REJECT
    assert rec.action == RecommendationAction.BLOCKED_FOR_SAFETY

    # Merge Target
    rec = build_tournament_recommendation(c1, r1, SafetyLane.SAFE_SHORTLIST_LANE, merge_target_id="c2")
    assert rec.action == RecommendationAction.MERGE_WITH_SIMILAR_CANDIDATE
