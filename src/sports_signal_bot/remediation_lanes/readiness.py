from typing import List
from sports_signal_bot.remediation_lanes.contracts import ClosedLoopReadinessGateRecord

def build_closed_loop_readiness_gates(gate_id: str, lane_ref: str, checkpoints: List[str]) -> ClosedLoopReadinessGateRecord:
    return ClosedLoopReadinessGateRecord(
        gate_id=gate_id,
        lane_ref=lane_ref,
        required_checkpoints=checkpoints,
        gate_status="passing"
    )

def evaluate_closed_loop_readiness(gate: ClosedLoopReadinessGateRecord) -> bool:
    return gate.gate_status == "passing" and not gate.blocking_reasons
