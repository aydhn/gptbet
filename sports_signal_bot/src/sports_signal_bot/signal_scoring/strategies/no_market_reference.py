import datetime
from typing import Any, Dict, List

from sports_signal_bot.signal_scoring.combine import (
    combine_signal_components, normalize_signal_score)
from sports_signal_bot.signal_scoring.contracts import (SignalCandidateRecord,
                                                        SignalComponentRecord,
                                                        SignalScoreRecord,
                                                        SignalStatus)
from sports_signal_bot.signal_scoring.strategies.balanced import \
    BalancedSignalScorer


class NoMarketReferenceFallbackScorer(BalancedSignalScorer):

    def name(self) -> str:
        return "no_market_reference"

    def describe(self) -> str:
        return "Safe fallback scorer when no market odds are available. Heavily relies on confidence."

    def score_signals(
        self, candidates: List[SignalCandidateRecord]
    ) -> List[SignalScoreRecord]:

        # We can inherit from Balanced, but we change weights and status
        original_weights = self.weights.copy()

        self.weights.update(
            {
                "edge_weight": 0.0,
                "confidence_weight": 2.0,  # Lean heavily on confidence
            }
        )

        results = super().score_signals(candidates)
        self.weights = original_weights

        for r in results:
            r.strategy_name = self.name()
            r.status = SignalStatus.NO_MARKET_REFERENCE

            # Since no edge, scores might be lower overall. Re-normalize to a tighter bound.
            r.normalized_score = normalize_signal_score(
                r.final_signal_score, min_expected=-1.0, max_expected=1.5
            )

        return results
