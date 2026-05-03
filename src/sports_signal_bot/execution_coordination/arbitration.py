import uuid
from typing import List, Optional
from src.sports_signal_bot.execution_coordination.contracts import (
    ContentionRecord, ArbitrationDecisionRecord, LaneScheduleRecord
)
from src.sports_signal_bot.execution_coordination.strategies import BaseCoordinationStrategy, BalancedMultiLaneFabricStrategy

class ArbitrationEngine:
    def __init__(self, strategy: Optional[BaseCoordinationStrategy] = None):
        self.strategy = strategy or BalancedMultiLaneFabricStrategy()
        self.arbitration_history: List[ArbitrationDecisionRecord] = []

    def arbitrate(self, contention: ContentionRecord, active_schedules: List[LaneScheduleRecord]) -> ArbitrationDecisionRecord:
        decision = self.strategy.determine_arbitration_outcome(contention, active_schedules)
        self.arbitration_history.append(decision)
        return decision
