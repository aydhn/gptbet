def detect_superseding_candidate(candidate_id: str, active_candidates: list) -> str:
    # Mock: check if any candidate in active_candidates supersedes the current one
    return None

def record_supersession(superseded_id: str, new_id: str) -> dict:
    return {
        "superseded_candidate": superseded_id,
        "superseding_candidate": new_id,
        "reason": "newer narrower patch replaces broader patch"
    }
