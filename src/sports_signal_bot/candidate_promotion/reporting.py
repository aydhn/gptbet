from typing import List, Dict, Any
from .contracts import CandidateManifest

def build_promotion_summary(manifest: CandidateManifest) -> Dict[str, Any]:
    """Builds a summary of the promotion run."""
    summary = {
        "processed_candidates": len(manifest.candidates),
        "promoted": 0,
        "held": 0,
        "revised": 0,
        "killed": 0
    }
    for decision in manifest.decisions:
        if decision.action.value == "promote_candidate_lane":
            summary["promoted"] += 1
        elif decision.action.value == "hold_candidate":
            summary["held"] += 1
        elif decision.action.value == "revise_candidate":
            summary["revised"] += 1
        elif decision.action.value == "kill_candidate":
            summary["killed"] += 1

    return summary
