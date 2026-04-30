from typing import List, Tuple, Dict, Any
from .contracts import TournamentCandidateRecord, CandidateComparisonRecord, SafetyLane, TournamentWarningRecord

def apply_tournament_constraints(
    candidates: List[TournamentCandidateRecord],
    comparisons: List[CandidateComparisonRecord],
    rules: Dict[str, Any]
) -> Tuple[List[CandidateComparisonRecord], List[TournamentWarningRecord]]:
    """Applies constraints to filter or penalize candidates before pareto ranking."""
    warnings = []
    valid_comparisons = []

    cand_map = {c.candidate_id: c for c in candidates}

    max_blast_radius = rules.get("max_blast_radius", 0.5)
    min_support = rules.get("min_support_strength", 0.3)

    for comp in comparisons:
        cand = cand_map.get(comp.candidate_id)
        if not cand:
            continue

        is_valid = True

        if cand.estimated_blast_radius > max_blast_radius:
            warnings.append(TournamentWarningRecord(
                warning_id="constraint_blast_radius",
                message=f"Candidate {cand.candidate_id} exceeds blast radius limit.",
                severity="high"
            ))
            # Mark for exploratory or block depending on strictness
            if rules.get("strict_blast_radius", True):
                is_valid = False
                comp.lane = SafetyLane.BLOCKED_LANE

        if cand.support_strength < min_support:
            warnings.append(TournamentWarningRecord(
                warning_id="constraint_low_support",
                message=f"Candidate {cand.candidate_id} has insufficient support.",
                severity="medium"
            ))
            # Move to exploratory rather than block
            if not comp.lane or comp.lane == SafetyLane.SAFE_SHORTLIST_LANE:
                comp.lane = SafetyLane.EXPLORATORY_LANE

        if is_valid:
            valid_comparisons.append(comp)

    return valid_comparisons, warnings

def summarize_constraint_failures(warnings: List[TournamentWarningRecord]) -> str:
    high_count = sum(1 for w in warnings if w.severity == "high")
    med_count = sum(1 for w in warnings if w.severity == "medium")
    return f"Constraint Failures: {high_count} High, {med_count} Medium"
