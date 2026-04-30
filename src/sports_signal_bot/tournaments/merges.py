from typing import List, Dict, Tuple
from .contracts import TournamentCandidateRecord

def detect_near_duplicate_candidates(
    candidate_a: TournamentCandidateRecord,
    candidate_b: TournamentCandidateRecord
) -> bool:
    """Detects if two candidates are near-duplicates that could be merged."""
    if candidate_a.target_component_family != candidate_b.target_component_family:
        return False

    # Check if scopes are identical or very similar
    scope_a_keys = set(candidate_a.scope.keys())
    scope_b_keys = set(candidate_b.scope.keys())
    if scope_a_keys != scope_b_keys:
        return False

    for k in scope_a_keys:
        if candidate_a.scope[k] != candidate_b.scope[k]:
            return False

    # Would also check patch payload similarity here in a real implementation
    return True

def propose_candidate_merge(
    candidates: List[TournamentCandidateRecord]
) -> Dict[str, str]:
    """Finds candidates that can be merged and proposes target IDs.
    Returns dict mapping candidate_id to merge_target_id.
    """
    merges = {}
    processed = set()

    for i, cand_a in enumerate(candidates):
        if cand_a.candidate_id in processed:
            continue

        for j, cand_b in enumerate(candidates[i+1:], i+1):
            if cand_b.candidate_id in processed:
                continue

            if detect_near_duplicate_candidates(cand_a, cand_b):
                # Propose merging B into A
                merges[cand_b.candidate_id] = cand_a.candidate_id
                processed.add(cand_b.candidate_id)

        processed.add(cand_a.candidate_id)

    return merges

def summarize_overlap_clusters(merges: Dict[str, str]) -> str:
    """Summarizes merge clusters."""
    if not merges:
        return "No overlapping candidates detected."

    clusters = {}
    for source, target in merges.items():
        if target not in clusters:
            clusters[target] = []
        clusters[target].append(source)

    summary = []
    for target, sources in clusters.items():
        summary.append(f"Target {target} can merge {len(sources)} candidates: {', '.join(sources)}")

    return "; ".join(summary)

def block_spam_candidate_flood(
    candidates: List[TournamentCandidateRecord]
) -> List[TournamentCandidateRecord]:
    """Blocks an overwhelming number of identical candidates."""
    merges = propose_candidate_merge(candidates)
    return [c for c in candidates if c.candidate_id not in merges]
