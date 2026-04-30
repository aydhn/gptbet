import uuid
from typing import List, Dict, Any
from .contracts import HandoffSummaryRecord

def generate_handoff_summary(results: List[Dict[str, Any]]) -> HandoffSummaryRecord:
    total = len(results)
    approve_count = sum(1 for r in results if r.get("decision") == "approve_handoff")
    hold_count = sum(1 for r in results if "hold" in str(r.get("decision", "")))
    reject_count = sum(1 for r in results if r.get("decision") == "reject_handoff")
    kill_count = sum(1 for r in results if r.get("decision") == "kill_candidate_before_handoff")
    bridge_ready_count = sum(1 for r in results if r.get("bridge_ready", False))
    activation_blocker_count = sum(1 for r in results if r.get("activation_blocked", False))
    superseded_count = sum(1 for r in results if r.get("is_superseded", False))

    return HandoffSummaryRecord(
        summary_id=str(uuid.uuid4()),
        total_candidates_evaluated=total,
        approve_count=approve_count,
        hold_count=hold_count,
        reject_count=reject_count,
        kill_count=kill_count,
        bridge_ready_count=bridge_ready_count,
        activation_blocker_count=activation_blocker_count,
        superseded_handoff_candidate_count=superseded_count,
        top_blocker_families=[],
        readiness_dimension_distribution={"pass": approve_count, "fail": reject_count + kill_count}
    )
