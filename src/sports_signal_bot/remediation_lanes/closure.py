from typing import List
from sports_signal_bot.remediation_lanes.contracts import (
    LoopClosureRecord,
    LoopClosureOutcome,
    RemediationLaneRecord
)

def build_loop_closure_packet(lane: RemediationLaneRecord, evidence_refs: List[str], outcome: LoopClosureOutcome) -> LoopClosureRecord:
    return LoopClosureRecord(
        closure_id=f"closure_{lane.lane_id}",
        lane_ref=lane.lane_id,
        outcome=outcome,
        evidence_refs=evidence_refs
    )

def verify_loop_closure(closure: LoopClosureRecord) -> bool:
    return closure.outcome in [LoopClosureOutcome.closed_clean, LoopClosureOutcome.closed_with_caveats]
