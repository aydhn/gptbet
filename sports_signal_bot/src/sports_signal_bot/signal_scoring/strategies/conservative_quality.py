import datetime
from typing import List, Dict, Any

from sports_signal_bot.signal_scoring.contracts import (
    SignalCandidateRecord, SignalScoreRecord, SignalComponentRecord, SignalStatus
)
from sports_signal_bot.signal_scoring.strategies.balanced import BalancedSignalScorer
from sports_signal_bot.signal_scoring.combine import combine_signal_components, normalize_signal_score

class ConservativeQualityScorer(BalancedSignalScorer):

    def name(self) -> str:
        return "conservative_quality"

    def describe(self) -> str:
        return "Heavily penalizes uncertainty, disagreement, and poor data quality."

    def score_signals(
        self, candidates: List[SignalCandidateRecord]
    ) -> List[SignalScoreRecord]:

        # We can inherit the logic from Balanced but inject harsher weights
        original_weights = self.weights.copy()

        self.weights.update({
            "uncertainty_penalty_weight": 2.5,
            "disagreement_penalty_weight": 2.5,
            "data_quality_penalty_weight": 3.0,
            "source_health_penalty_weight": 2.0
        })

        results = super().score_signals(candidates)

        # Restore (though it's instantiated per run usually)
        self.weights = original_weights

        for r in results:
            r.strategy_name = self.name()
            # Be harsher on status
            if r.normalized_score is not None and r.normalized_score < self.thresholds.get("conservative_weak_threshold", 50.0):
                if r.status == SignalStatus.SCORED:
                    r.status = SignalStatus.INSUFFICIENT_QUALITY

        return results
