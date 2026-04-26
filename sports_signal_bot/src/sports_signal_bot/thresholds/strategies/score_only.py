from typing import Dict, Any, List, Tuple
import numpy as np
from .base import BaseThresholdOptimizer
from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord
from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord

class ScoreOnlyThresholdOptimizer(BaseThresholdOptimizer):
    def generate_grid(self) -> List[Dict[str, float]]:
        bounds = self.config.get("score_threshold_bounds", [0.0, 1.0])
        steps = self.config.get("grid_steps", 20)

        # Guard for potentially missing values
        if not bounds or len(bounds) < 2:
             bounds = [0.0, 1.0]

        grid = []
        for val in np.linspace(bounds[0], bounds[1], steps):
            grid.append({"score_threshold": float(val)})

        return grid

    def apply_threshold(self, signals: List[SignalScoreRecord], params: Dict[str, float]) -> Tuple[List[SignalScoreRecord], List[SignalScoreRecord]]:
        score_threshold = params.get("score_threshold", 0.0)

        accepted = []
        rejected = []

        for sig in signals:
            if sig.final_signal_score >= score_threshold:
                accepted.append(sig)
            else:
                rejected.append(sig)

        return accepted, rejected
