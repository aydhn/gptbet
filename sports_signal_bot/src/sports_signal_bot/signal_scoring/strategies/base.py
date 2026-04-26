from abc import ABC, abstractmethod
from typing import Dict, Any, List

from sports_signal_bot.signal_scoring.contracts import SignalCandidateRecord, SignalScoreRecord

class BaseSignalScorer(ABC):

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.weights = config.get("weights", {})
        self.thresholds = config.get("thresholds", {})
        self.policies = config.get("policies", {})

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass

    @abstractmethod
    def score_signals(
        self, candidates: List[SignalCandidateRecord]
    ) -> List[SignalScoreRecord]:
        pass
