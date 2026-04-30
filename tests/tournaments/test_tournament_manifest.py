import pytest
from src.sports_signal_bot.tournaments.contracts import (
    TournamentRequestRecord, TournamentBatchRecord, TournamentUniverseRecord, TournamentFamily,
    ParetoFrontRecord, TournamentRankingRecord, CandidateScorecardRecord, TournamentRecommendationRecord,
    RecommendationAction, ShortlistTier, SafetyLane
)
from src.sports_signal_bot.tournaments.manifests import build_tournament_manifest

def test_manifest_building():
    universe = TournamentUniverseRecord(
        universe_id="u1", replay_window={"start": "2023-01-01T00:00:00", "end": "2023-01-02T00:00:00"},
        target_sports=["football"], target_markets=["O/U"], baseline_snapshot_id="b1",
        release_channel_base="main", gate_requirements_profile="default"
    )

    request = TournamentRequestRecord(
        tournament_id="t1", tournament_family=TournamentFamily.THRESHOLD_TOURNAMENT,
        target_component_family="threshold", audience_profile="operator", candidate_ids=["c1"],
        baseline_ref="b1", simulation_mode="comparative_slot_replay", comparison_universe=universe,
        selection_policy="default"
    )

    batch = TournamentBatchRecord(batch_id="b1", tournament_id="t1", universe_id="u1", candidates=[])

    rankings = [
        TournamentRankingRecord(candidate_id="c1", pareto_front=1, secondary_rank=1, lane=SafetyLane.SAFE_SHORTLIST_LANE, explanation="")
    ]

    recommendations = [
        TournamentRecommendationRecord(recommendation_id="r1", candidate_id="c1", action=RecommendationAction.SHORTLIST_FOR_APPROVAL, tier=ShortlistTier.TIER_1_REVIEW_NOW, rationale="")
    ]

    manifest = build_tournament_manifest(request, batch, [], rankings, [], recommendations)

    assert manifest.tournament_id == "t1"
    assert len(manifest.shortlists) == 1
    assert manifest.shortlists[0].tier == ShortlistTier.TIER_1_REVIEW_NOW
    assert manifest.shortlists[0].ranked_candidates[0].candidate_id == "c1"
