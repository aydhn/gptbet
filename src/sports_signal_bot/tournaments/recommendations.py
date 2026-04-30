from typing import List, Dict, Any, Optional
from .contracts import (
    TournamentCandidateRecord,
    TournamentRankingRecord,
    TournamentRecommendationRecord,
    RecommendationAction,
    ShortlistTier,
    SafetyLane
)
import uuid

def classify_shortlist_tier(
    ranking: TournamentRankingRecord,
    lane: SafetyLane
) -> ShortlistTier:
    """Maps rankings and lanes to shortlist tiers."""
    if lane == SafetyLane.BLOCKED_LANE or lane == SafetyLane.INVALID_LANE:
        return ShortlistTier.TIER_4_REJECT

    if lane == SafetyLane.SAFE_SHORTLIST_LANE:
        if ranking.pareto_front == 1:
            return ShortlistTier.TIER_1_REVIEW_NOW
        return ShortlistTier.TIER_2_GOOD_BUT_NEEDS_MORE_EVIDENCE

    if lane == SafetyLane.ADVISORY_LANE:
        return ShortlistTier.TIER_2_GOOD_BUT_NEEDS_MORE_EVIDENCE

    return ShortlistTier.TIER_3_EXPLORATORY

def explain_recommendation_reason(action: RecommendationAction, tier: ShortlistTier, lane: SafetyLane) -> str:
    """Generates a rationale for the recommendation."""
    if action == RecommendationAction.BLOCKED_FOR_SAFETY:
        return "Candidate is blocked due to safety constraint violations."
    if action == RecommendationAction.SHORTLIST_FOR_APPROVAL:
        return "Candidate is on the pareto front, in a safe lane, and ready for approval."
    if action == RecommendationAction.SHORTLIST_FOR_REVIEW:
        return "Candidate shows promise but requires manual review."
    if action == RecommendationAction.KEEP_AS_ADVISORY:
        return "Candidate provides advisory value but is not safe for direct action."
    if action == RecommendationAction.REQUEST_ADDITIONAL_SIMULATION:
        return "Candidate needs more simulation evidence to prove viability."
    if action == RecommendationAction.MERGE_WITH_SIMILAR_CANDIDATE:
        return "Candidate is largely redundant and should be merged."
    return "Candidate is rejected based on evaluation criteria."

def build_tournament_recommendation(
    candidate: TournamentCandidateRecord,
    ranking: TournamentRankingRecord,
    lane: SafetyLane,
    merge_target_id: Optional[str] = None
) -> TournamentRecommendationRecord:
    """Builds the final recommendation for a candidate."""

    tier = classify_shortlist_tier(ranking, lane)
    action = RecommendationAction.REJECT_CANDIDATE

    if merge_target_id:
        action = RecommendationAction.MERGE_WITH_SIMILAR_CANDIDATE
    elif lane == SafetyLane.BLOCKED_LANE:
        action = RecommendationAction.BLOCKED_FOR_SAFETY
    elif tier == ShortlistTier.TIER_1_REVIEW_NOW:
        action = RecommendationAction.SHORTLIST_FOR_APPROVAL if candidate.support_strength >= 0.8 else RecommendationAction.SHORTLIST_FOR_REVIEW
    elif tier == ShortlistTier.TIER_2_GOOD_BUT_NEEDS_MORE_EVIDENCE:
        action = RecommendationAction.KEEP_AS_ADVISORY if lane == SafetyLane.ADVISORY_LANE else RecommendationAction.REQUEST_ADDITIONAL_SIMULATION
    elif tier == ShortlistTier.TIER_3_EXPLORATORY:
        action = RecommendationAction.REQUEST_ADDITIONAL_SIMULATION

    rationale = explain_recommendation_reason(action, tier, lane)

    return TournamentRecommendationRecord(
        recommendation_id=str(uuid.uuid4()),
        candidate_id=candidate.candidate_id,
        action=action,
        tier=tier,
        rationale=rationale,
        merge_target_id=merge_target_id
    )

def generate_all_recommendations(
    candidates: List[TournamentCandidateRecord],
    rankings: List[TournamentRankingRecord],
    merges: Dict[str, str]
) -> List[TournamentRecommendationRecord]:
    """Generates recommendations for all candidates."""
    recs = []
    cand_map = {c.candidate_id: c for c in candidates}

    for rank in rankings:
        cand = cand_map.get(rank.candidate_id)
        if not cand:
            continue

        merge_target = merges.get(rank.candidate_id)
        recs.append(build_tournament_recommendation(cand, rank, rank.lane, merge_target))

    return recs
