from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord
from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord
import numpy as np

class BaseThresholdOptimizer(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def generate_grid(self) -> List[Dict[str, float]]:
        """Generate grid of thresholds to evaluate"""
        pass

    @abstractmethod
    def apply_threshold(self, signals: List[SignalScoreRecord], params: Dict[str, float]) -> Tuple[List[SignalScoreRecord], List[SignalScoreRecord]]:
        """Return (accepted_signals, rejected_signals)"""
        pass
