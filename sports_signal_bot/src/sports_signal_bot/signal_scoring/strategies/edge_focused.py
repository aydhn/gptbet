import datetime
from typing import Any, Dict, List

from sports_signal_bot.signal_scoring.combine import (
    combine_signal_components, normalize_signal_score)
from sports_signal_bot.signal_scoring.contracts import (SignalCandidateRecord,
                                                        SignalComponentRecord,
                                                        SignalScoreRecord,
                                                        SignalStatus)
from sports_signal_bot.signal_scoring.edge import compute_edge
from sports_signal_bot.signal_scoring.strategies.base import BaseSignalScorer


class EdgeFocusedScorer(BaseSignalScorer):

    def name(self) -> str:
        return "edge_focused"

    def describe(self) -> str:
        return "Focuses primarily on the calculated edge against market implied probabilities."

    def score_signals(
        self, candidates: List[SignalCandidateRecord]
    ) -> List[SignalScoreRecord]:

        results = []

        # Override weights for this strategy
        weights = {
            "edge_weight": 2.0,
            "confidence_weight": 0.5,
            "uncertainty_penalty_weight": 0.5,
            "disagreement_penalty_weight": 0.5,
            "data_quality_penalty_weight": 0.5,
            "source_health_penalty_weight": 0.5,
            "regime_adjustment_weight": 0.0,
        }

        for cand in candidates:
            # 1. Edge computation
            edge = compute_edge(cand.final_probability, cand.market_implied_probability)

            # Simple confidence
            conf = cand.final_probability if cand.final_probability > 0 else 0.0

            comps = SignalComponentRecord(edge_estimate=edge, confidence_score=conf)

            # Combine
            raw_score = combine_signal_components(comps, weights)
            norm_score = normalize_signal_score(raw_score)

            status = SignalStatus.SCORED
            if cand.market_implied_probability is None:
                status = SignalStatus.NO_MARKET_REFERENCE

            record = SignalScoreRecord(
                event_id=cand.event_id,
                sport=cand.sport,
                market_type=cand.market_type,
                selection=cand.selection,
                final_probability=cand.final_probability,
                market_implied_probability=cand.market_implied_probability,
                components=comps,
                final_signal_score=raw_score,
                normalized_score=norm_score,
                strategy_name=self.name(),
                status=status,
                created_at_utc=datetime.datetime.utcnow(),
            )
            results.append(record)

        return results
