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

class ConservativeCoordinationFabricStrategy(BaseCoordinationStrategy):
    def name(self) -> str:
        return "ConservativeCoordinationFabricStrategy"

    def determine_arbitration_outcome(self, contention: ContentionRecord, active_schedules: List[LaneScheduleRecord]) -> ArbitrationDecisionRecord:
        # Heavily biased towards serialization
        lane_a = contention.involved_lane_refs[0] if contention.involved_lane_refs else "unknown"
        lane_b = contention.involved_lane_refs[1] if len(contention.involved_lane_refs) > 1 else "unknown"

        return ArbitrationDecisionRecord(
            arbitration_id=f"arb_{uuid.uuid4().hex[:8]}",
            contention_id=contention.contention_id,
            decision_type="serialize_lanes",
            winning_lane_refs=[lane_a],
            deferred_lane_refs=[lane_b],
            reason="Conservative strategy defaults to serial execution for any contention."
        )

    def compute_fabric_status(self, active_contentions: int, backlog_pressure: float, token_broker_status: TokenBrokerStatus) -> FabricStatus:
        if backlog_pressure > 0.5 or active_contentions > 2 or token_broker_status != TokenBrokerStatus.BROKER_HEALTHY:
            return FabricStatus.FABRIC_CAUTIOUS
        return FabricStatus.FABRIC_NORMAL
