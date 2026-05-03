from typing import List
from .contracts import (
    RemediationLaneRecord, BoundedExecutionTokenRecord, ClosedLoopReadinessGateRecord,
    LaneCheckpointRecord, LaneStopConditionRecord, LoopClosureRecord, ClosureOutcome
)
import uuid

def evaluate_closed_loop_readiness(lane: RemediationLaneRecord, token: BoundedExecutionTokenRecord) -> ClosedLoopReadinessGateRecord:
    blockers = []

    if token.status != "active":
        blockers.append("invalid_or_expired_token")

    if not lane.rollback_binding.rollback_playbook_ref:
        blockers.append("missing_rollback_binding")

    status = "passed" if not blockers else "blocked"

    return ClosedLoopReadinessGateRecord(
        gate_id=f"gate_{uuid.uuid4().hex[:8]}",
        lane_ref=lane.lane_id,
        required_checkpoints=["post_execution_health_check"],
        required_observability_signals=["latency_normal", "error_rate_low"],
        required_rollback_checks=["rollback_script_reachable"],
        gate_status=status,
        blocking_reasons=blockers
    )

def verify_loop_closure(lane: RemediationLaneRecord, checkpoints: List[LaneCheckpointRecord], stops: List[LaneStopConditionRecord], used_rollback: bool) -> LoopClosureRecord:
    triggered_stops = sum(1 for s in stops if s.triggered)
    met_checkpoints = sum(1 for c in checkpoints if c.is_aligned_with_expectation)

    if triggered_stops > 0 or used_rollback:
        outcome = ClosureOutcome.closed_with_caveats if used_rollback else ClosureOutcome.closure_failed
    elif met_checkpoints < len(checkpoints) and len(checkpoints) > 0:
        outcome = ClosureOutcome.closure_incomplete
    else:
        outcome = ClosureOutcome.closed_clean

    return LoopClosureRecord(
        closure_id=f"closure_{uuid.uuid4().hex[:8]}",
        lane_ref=lane.lane_id,
        outcome=outcome,
        checkpoints_met=met_checkpoints,
        total_checkpoints=len(checkpoints),
        stop_conditions_triggered=triggered_stops,
        rollback_used=used_rollback,
        evidence_refs=[c.checkpoint_id for c in checkpoints],
        warnings=["Stop condition triggered during lane"] if triggered_stops > 0 else []
    )
