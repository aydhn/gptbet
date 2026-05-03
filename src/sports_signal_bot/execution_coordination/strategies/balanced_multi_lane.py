import uuid
from typing import List
from sports_signal_bot.execution_coordination.strategies.base import BaseCoordinationStrategy
from sports_signal_bot.execution_coordination.contracts import (
    LaneScheduleRecord,
    ContentionRecord,
    ArbitrationDecisionRecord,
    TokenBrokerStatus,
    FabricStatus,
    PriorityBand,
    ContentionSeverity
)

class BalancedMultiLaneFabricStrategy(BaseCoordinationStrategy):
    def name(self) -> str:
        return "BalancedMultiLaneFabricStrategy"

    def determine_arbitration_outcome(self, contention: ContentionRecord, active_schedules: List[LaneScheduleRecord]) -> ArbitrationDecisionRecord:
        if contention.severity in [ContentionSeverity.CRITICAL, ContentionSeverity.HIGH]:
             return ArbitrationDecisionRecord(
                arbitration_id=f"arb_{uuid.uuid4().hex[:8]}",
                contention_id=contention.contention_id,
                decision_type="serialize_lanes",
                winning_lane_refs=[contention.involved_lane_refs[0]] if contention.involved_lane_refs else [],
                deferred_lane_refs=contention.involved_lane_refs[1:],
                reason="High severity contention requires serialization."
             )
        else:
             return ArbitrationDecisionRecord(
                arbitration_id=f"arb_{uuid.uuid4().hex[:8]}",
                contention_id=contention.contention_id,
                decision_type="allow_parallel_execution",
                winning_lane_refs=contention.involved_lane_refs,
                deferred_lane_refs=[],
                reason="Low/Medium severity contention allows bounded parallel execution."
             )


    def compute_fabric_status(self, active_contentions: int, backlog_pressure: float, token_broker_status: TokenBrokerStatus) -> FabricStatus:
        if active_contentions > 10 or backlog_pressure > 0.8:
            return FabricStatus.FABRIC_THROTTLED
        elif active_contentions > 5:
            return FabricStatus.FABRIC_CONTENTION_HEAVY
        return FabricStatus.FABRIC_NORMAL
