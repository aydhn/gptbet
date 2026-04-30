from typing import List, Dict, Any
from .contracts import TournamentCandidateRecord, CandidateComparisonRecord, ParetoFrontRecord, TournamentRankingRecord, SafetyLane
from ..simulation.contracts import RiskLevel

def compute_secondary_priority(
    candidate: TournamentCandidateRecord,
    comparison: CandidateComparisonRecord,
    rules: Dict[str, Any]
) -> float:
    """Computes a scalar priority score for ranking candidates within the same pareto front."""
    score = 0.0

    # Lower risk is better
    risk_weights = {
        RiskLevel.LOW: 10.0,
        RiskLevel.MEDIUM: 5.0,
        RiskLevel.HIGH: -5.0,
        RiskLevel.CRITICAL: -20.0
    }
    score += risk_weights.get(candidate.risk_level, 0.0)

    # Narrower scope / blast radius is preferred
    score -= (candidate.estimated_blast_radius * rules.get("blast_radius_penalty_weight", 10.0))

    # Higher support is preferred
    score += (candidate.support_strength * rules.get("support_weight", 5.0))

    return score

def explain_tiebreak_result(candidate_id: str, score: float) -> str:
    return f"Candidate {candidate_id} scored {score:.2f} on secondary tiebreak factors (risk, scope, support)."

def rank_within_front(
    front: ParetoFrontRecord,
    candidates: Dict[str, TournamentCandidateRecord],
    comparisons: Dict[str, CandidateComparisonRecord],
    rules: Dict[str, Any]
) -> List[TournamentRankingRecord]:
    """Ranks candidates within a specific pareto front."""
    scored_candidates = []

    for cid in front.candidate_ids:
        cand = candidates.get(cid)
        comp = comparisons.get(cid)
        if not cand or not comp:
            continue

        score = compute_secondary_priority(cand, comp, rules)
        scored_candidates.append((score, cid, comp.lane))

    # Sort by score descending
    scored_candidates.sort(key=lambda x: x[0], reverse=True)

    rankings = []
    for rank, (score, cid, lane) in enumerate(scored_candidates, 1):
        rankings.append(TournamentRankingRecord(
            candidate_id=cid,
            pareto_front=front.front_index,
            secondary_rank=rank,
            lane=lane or SafetyLane.EXPLORATORY_LANE,
            total_score=score,
            explanation=explain_tiebreak_result(cid, score)
        ))

    return rankings

def build_final_shortlist_order(
    fronts: List[ParetoFrontRecord],
    candidates: List[TournamentCandidateRecord],
    comparisons: List[CandidateComparisonRecord],
    rules: Dict[str, Any]
) -> List[TournamentRankingRecord]:
    """Builds the final ranked list across all fronts."""
    cand_map = {c.candidate_id: c for c in candidates}
    comp_map = {c.candidate_id: c for c in comparisons}

    all_rankings = []

    for front in fronts:
        rankings = rank_within_front(front, cand_map, comp_map, rules)
        all_rankings.extend(rankings)

    return all_rankings
