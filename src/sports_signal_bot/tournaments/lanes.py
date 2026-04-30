from typing import List, Dict, Any
from .contracts import TournamentCandidateRecord, CandidateComparisonRecord, SafetyLane
from ..simulation.contracts import RiskLevel

def classify_candidate_safety_lane(
    candidate: TournamentCandidateRecord,
    comparison: CandidateComparisonRecord,
    is_pareto_front: bool,
    rules: Dict[str, Any]
) -> SafetyLane:
    """Classifies a candidate into a safety lane based on risk, support, and pareto status."""

    # If already blocked or marked invalid by constraints, keep it
    if comparison.lane in [SafetyLane.BLOCKED_LANE, SafetyLane.INVALID_LANE]:
        return comparison.lane

    if candidate.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
        if candidate.estimated_blast_radius > rules.get("high_risk_blast_threshold", 0.3):
            return SafetyLane.BLOCKED_LANE
        return SafetyLane.ADVISORY_LANE

    if candidate.support_strength < rules.get("safe_support_threshold", 0.5):
        return SafetyLane.EXPLORATORY_LANE

    if not is_pareto_front:
        if candidate.risk_level == RiskLevel.LOW and candidate.support_strength > rules.get("advisory_support_threshold", 0.7):
            return SafetyLane.ADVISORY_LANE
        return SafetyLane.EXPLORATORY_LANE

    return SafetyLane.SAFE_SHORTLIST_LANE

def separate_exploratory_candidates(
    comparisons: List[CandidateComparisonRecord]
) -> List[CandidateComparisonRecord]:
    """Filters out non-exploratory candidates."""
    return [c for c in comparisons if c.lane == SafetyLane.EXPLORATORY_LANE]

def block_unsafe_shortlisting(
    comparison: CandidateComparisonRecord
) -> CandidateComparisonRecord:
    """Ensures unsafe candidates aren't in the shortlist lane."""
    if comparison.lane == SafetyLane.SAFE_SHORTLIST_LANE and getattr(comparison, '_unsafe_flag', False):
        comparison.lane = SafetyLane.BLOCKED_LANE
    return comparison
