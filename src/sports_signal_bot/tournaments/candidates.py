from typing import List, Dict, Any, Tuple
from .contracts import TournamentCandidateRecord, TournamentWarningRecord

def normalize_candidate_for_tournament(
    raw_candidate: Dict[str, Any]
) -> TournamentCandidateRecord:
    """Normalizes a raw suggestion/patch into a TournamentCandidateRecord."""
    return TournamentCandidateRecord(**raw_candidate)

def group_candidates_by_target(
    candidates: List[TournamentCandidateRecord]
) -> Dict[str, List[TournamentCandidateRecord]]:
    """Groups candidates by target component family."""
    groups: Dict[str, List[TournamentCandidateRecord]] = {}
    for candidate in candidates:
        target = candidate.target_component_family
        if target not in groups:
            groups[target] = []
        groups[target].append(candidate)
    return groups

def detect_scope_mismatch(
    candidate1: TournamentCandidateRecord,
    candidate2: TournamentCandidateRecord
) -> bool:
    """Detects if two candidates have mismatched scope granularity."""
    return candidate1.scope.keys() != candidate2.scope.keys()

def block_incomparable_candidates(
    candidates: List[TournamentCandidateRecord]
) -> Tuple[List[TournamentCandidateRecord], List[TournamentCandidateRecord], List[TournamentWarningRecord]]:
    """Blocks candidates that cannot be compared to the main group."""
    if not candidates:
        return [], [], []

    main_target = candidates[0].target_component_family
    comparable = []
    blocked = []
    warnings = []

    for candidate in candidates:
        if candidate.target_component_family == main_target:
            comparable.append(candidate)
        else:
            blocked.append(candidate)
            warnings.append(TournamentWarningRecord(
                warning_id="blocked_incomparable",
                message=f"Candidate {candidate.candidate_id} blocked due to target mismatch.",
                severity="critical"
            ))

    return comparable, blocked, warnings

def harmonize_metric_spaces(
    candidates: List[TournamentCandidateRecord],
    metric_configs: Dict[str, Any]
) -> List[TournamentCandidateRecord]:
    """Placeholder for metric harmonization."""
    return candidates
