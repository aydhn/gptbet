from typing import Any, Dict, List, Tuple

import numpy as np

from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord
from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord

from .base import BaseThresholdOptimizer


class ScoreAndEdgeThresholdOptimizer(BaseThresholdOptimizer):
    def generate_grid(self) -> List[Dict[str, float]]:
        score_bounds = self.config.get("score_threshold_bounds", [0.0, 1.0])
        edge_bounds = self.config.get("edge_threshold_bounds", [0.0, 0.1])
        steps = self.config.get("grid_steps", 10)

        if not score_bounds or len(score_bounds) < 2:
            score_bounds = [0.0, 1.0]
        if not edge_bounds or len(edge_bounds) < 2:
            edge_bounds = [0.0, 0.1]

        grid = []
        for s_val in np.linspace(score_bounds[0], score_bounds[1], steps):
            for e_val in np.linspace(edge_bounds[0], edge_bounds[1], steps):
                grid.append(
                    {"score_threshold": float(s_val), "edge_threshold": float(e_val)}
                )

        return grid

    def apply_threshold(
        self, signals: List[SignalScoreRecord], params: Dict[str, float]
    ) -> Tuple[List[SignalScoreRecord], List[SignalScoreRecord]]:
        score_threshold = params.get("score_threshold", 0.0)
        edge_threshold = params.get("edge_threshold", 0.0)

        accepted = []
        rejected = []

        for sig in signals:
            if (
                sig.final_signal_score >= score_threshold
                and sig.components.edge_estimate >= edge_threshold
            ):
                accepted.append(sig)
            else:
                rejected.append(sig)

        return accepted, rejected
