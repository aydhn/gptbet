from typing import Dict, Any, List
from .contracts import HandoffCandidateRecord

def compare_handoff_candidates(candidate_a: Dict[str, Any], candidate_b: Dict[str, Any]) -> str:
    # Returns the candidate_release_id of the stronger candidate
    score_a = candidate_a.get("readiness_score", 0)
    score_b = candidate_b.get("readiness_score", 0)

    if score_a > score_b:
        return candidate_a.get("candidate_release_id", "A")
    elif score_b > score_a:
        return candidate_b.get("candidate_release_id", "B")

    # Tie break: narrower scope wins
    scope_a = candidate_a.get("scope", "broad")
    scope_b = candidate_b.get("scope", "broad")
    if scope_a == "narrow" and scope_b != "narrow":
         return candidate_a.get("candidate_release_id", "A")
    if scope_b == "narrow" and scope_a != "narrow":
         return candidate_b.get("candidate_release_id", "B")

    return candidate_a.get("candidate_release_id", "A") # default to A on absolute tie

def resolve_handoff_supersession(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Marks weaker candidates in the same family as superseded
    family_map = {}
    for c in candidates:
        fam = c.get("target_component_family")
        if fam not in family_map:
            family_map[fam] = []
        family_map[fam].append(c)

    resolved_candidates = []
    for fam, fam_candidates in family_map.items():
        if len(fam_candidates) == 1:
            resolved_candidates.extend(fam_candidates)
            continue

        # Find best
        best = fam_candidates[0]
        for other in fam_candidates[1:]:
             winner_id = compare_handoff_candidates(best, other)
             if winner_id == other.get("candidate_release_id"):
                 best = other

        for c in fam_candidates:
            if c.get("candidate_release_id") != best.get("candidate_release_id"):
                c["is_superseded"] = True
                c["superseded_by"] = best.get("candidate_release_id")
            resolved_candidates.append(c)

    return resolved_candidates
