import uuid
from typing import List
from src.sports_signal_bot.execution_coordination.strategies.base import BaseCoordinationStrategy
from src.sports_signal_bot.execution_coordination.contracts import (
    LaneScheduleRecord,
    ContentionRecord,
    ArbitrationDecisionRecord,
    TokenBrokerStatus,
    FabricStatus,
    PriorityBand
)

class RollbackClosurePriorityStrategy(BaseCoordinationStrategy):
    def name(self) -> str:
        return "RollbackClosurePriorityStrategy"

    def determine_arbitration_outcome(self, contention: ContentionRecord, active_schedules: List[LaneScheduleRecord]) -> ArbitrationDecisionRecord:
        # Prioritize rollback or closure lanes over anything else
        # Simple heuristic for demonstration: assume lane_a is rollback if the name contains 'rollback' (in a real implementation we'd check priority bands)

        winner = contention.involved_lane_refs[0] if contention.involved_lane_refs else "unknown"
        deferred = contention.involved_lane_refs[1:]

        for lane_ref in contention.involved_lane_refs:
            if "rollback" in lane_ref or "closure" in lane_ref:
                winner = lane_ref
                deferred = [l for l in contention.involved_lane_refs if l != winner]
                break

        return ArbitrationDecisionRecord(
            arbitration_id=f"arb_{uuid.uuid4().hex[:8]}",
            contention_id=contention.contention_id,
            decision_type="reserve_for_rollback_or_closure",
            winning_lane_refs=[winner],
            deferred_lane_refs=deferred,
            reason="Priority given to rollback/closure."
        )

    def compute_fabric_status(self, active_contentions: int, backlog_pressure: float, token_broker_status: TokenBrokerStatus) -> FabricStatus:
        if backlog_pressure > 0.6:
            return FabricStatus.FABRIC_ROLLBACK_PRIORITY_MODE
        return FabricStatus.FABRIC_NORMAL
