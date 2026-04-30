from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sports_signal_bot.staged_channels.contracts import RolloutDecisionRecord, CandidateChannelRecord, CandidateFleetRecord

class BaseStagedChannelStrategy(ABC):
    @abstractmethod
    def evaluate_progression(self, candidate_id: str, current_stage: str, metrics: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def handle_fleet_conflicts(self, fleet: CandidateFleetRecord, candidate_id: str) -> bool:
        pass
