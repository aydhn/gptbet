from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from sports_signal_bot.execution_coordination.contracts import (
    LaneScheduleRecord,
    ContentionRecord,
    ArbitrationDecisionRecord,
    TokenBrokerStatus,
    FabricStatus,
    PriorityBand
)

class BaseCoordinationStrategy(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def determine_arbitration_outcome(self, contention: ContentionRecord, active_schedules: List[LaneScheduleRecord]) -> ArbitrationDecisionRecord:
        pass

    @abstractmethod
    def compute_fabric_status(self, active_contentions: int, backlog_pressure: float, token_broker_status: TokenBrokerStatus) -> FabricStatus:
        pass
