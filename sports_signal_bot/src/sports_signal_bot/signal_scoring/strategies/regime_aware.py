import datetime
from typing import List, Dict, Any

from sports_signal_bot.signal_scoring.contracts import (
    SignalCandidateRecord, SignalScoreRecord, SignalComponentRecord, SignalStatus
)
from sports_signal_bot.signal_scoring.strategies.balanced import BalancedSignalScorer
from sports_signal_bot.signal_scoring.regime import compute_regime_adjustment
from sports_signal_bot.signal_scoring.combine import combine_signal_components, normalize_signal_score

class RegimeAwareSignalScorer(BalancedSignalScorer):

    def name(self) -> str:
        return "regime_aware"

    def describe(self) -> str:
        return "Extends Balanced scorer by applying regime-based boosts and penalties."

    def score_signals(
        self, candidates: List[SignalCandidateRecord]
    ) -> List[SignalScoreRecord]:

        # We start by getting the balanced scores
        results = super().score_signals(candidates)

        # Now apply regime adjustments
        for r, c in zip(results, candidates):
            r.strategy_name = self.name()

            assignments = c.metadata.get("regime_assignments", [])
            regime_adj = compute_regime_adjustment(assignments, self.policies.get("regime", {}))

            # Update component
            r.components.regime_adjustment = regime_adj

            # Recompute score
            raw_score = combine_signal_components(r.components, self.weights)
            norm_score = normalize_signal_score(raw_score)

            r.final_signal_score = raw_score
            r.normalized_score = norm_score

        return results
