from typing import Any, Dict, List, Tuple

import numpy as np

from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord
from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord

from .base import BaseThresholdOptimizer


class CoverageBalancedOptimizer(BaseThresholdOptimizer):
    def generate_grid(self) -> List[Dict[str, float]]:
        score_bounds = self.config.get("score_threshold_bounds", [0.2, 0.8])
        steps = self.config.get("grid_steps", 20)

        if not score_bounds or len(score_bounds) < 2:
            score_bounds = [0.2, 0.8]

        grid = []
        for val in np.linspace(score_bounds[0], score_bounds[1], steps):
            grid.append({"score_threshold": float(val)})

        return grid

    def apply_threshold(
        self, signals: List[SignalScoreRecord], params: Dict[str, float]
    ) -> Tuple[List[SignalScoreRecord], List[SignalScoreRecord]]:
        score_threshold = params.get("score_threshold", 0.0)

        accepted = []
        rejected = []

        for sig in signals:
            if sig.final_signal_score >= score_threshold:
                accepted.append(sig)
            else:
                rejected.append(sig)

        return accepted, rejected
