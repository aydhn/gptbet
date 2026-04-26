from typing import Dict, Any, List, Tuple
import numpy as np
from .base import BaseThresholdOptimizer
from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord
from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord

class ConservativeQualityOptimizer(BaseThresholdOptimizer):
    def generate_grid(self) -> List[Dict[str, float]]:
        score_bounds = self.config.get("score_threshold_bounds", [0.4, 0.9])
        steps = self.config.get("grid_steps", 15)

        if not score_bounds or len(score_bounds) < 2:
            score_bounds = [0.4, 0.9]

        grid = []
        for val in np.linspace(score_bounds[0], score_bounds[1], steps):
            grid.append({"score_threshold": float(val)})

        return grid

    def apply_threshold(self, signals: List[SignalScoreRecord], params: Dict[str, float]) -> Tuple[List[SignalScoreRecord], List[SignalScoreRecord]]:
        score_threshold = params.get("score_threshold", 0.0)

        # Conservative guards
        max_uncertainty = self.config.get("hard_max_uncertainty", 0.3)
        max_data_quality_penalty = self.config.get("hard_max_dq_penalty", 0.2)

        accepted = []
        rejected = []

        for sig in signals:
            if (sig.final_signal_score >= score_threshold and
                sig.components.uncertainty_penalty <= max_uncertainty and
                sig.components.data_quality_penalty <= max_data_quality_penalty):
                accepted.append(sig)
            else:
                rejected.append(sig)

        return accepted, rejected
