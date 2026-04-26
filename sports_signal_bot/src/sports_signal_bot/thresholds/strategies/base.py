from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

import numpy as np

from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord
from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord


class BaseThresholdOptimizer(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def generate_grid(self) -> List[Dict[str, float]]:
        """Generate grid of thresholds to evaluate"""
        pass

    @abstractmethod
    def apply_threshold(
        self, signals: List[SignalScoreRecord], params: Dict[str, float]
    ) -> Tuple[List[SignalScoreRecord], List[SignalScoreRecord]]:
        """Return (accepted_signals, rejected_signals)"""
        pass
