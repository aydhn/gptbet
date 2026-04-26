import datetime
from typing import Any, Dict, List

from sports_signal_bot.signal_scoring.combine import (
    combine_signal_components, normalize_signal_score)
from sports_signal_bot.signal_scoring.confidence import (
    compute_confidence_score, compute_entropy, compute_top_class_gap)
from sports_signal_bot.signal_scoring.contracts import (SignalCandidateRecord,
                                                        SignalComponentRecord,
                                                        SignalScoreRecord,
                                                        SignalStatus)
from sports_signal_bot.signal_scoring.data_quality import \
    compute_data_quality_penalty
from sports_signal_bot.signal_scoring.disagreement import \
    compute_disagreement_penalty
from sports_signal_bot.signal_scoring.edge import compute_edge
from sports_signal_bot.signal_scoring.source_health import \
    compute_source_health_penalty
from sports_signal_bot.signal_scoring.strategies.base import BaseSignalScorer
from sports_signal_bot.signal_scoring.uncertainty import \
    compute_uncertainty_penalty


class BalancedSignalScorer(BaseSignalScorer):

    def name(self) -> str:
        return "balanced"

    def describe(self) -> str:
        return "A balanced strategy that considers edge, confidence, and all penalties."

    def score_signals(
        self, candidates: List[SignalCandidateRecord]
    ) -> List[SignalScoreRecord]:

        results = []

        for cand in candidates:
            # Metadata unpacking
            entropy_thresholds = self.thresholds.get("entropy", {})
            disagreement_thresholds = self.thresholds.get("disagreement", {})
            dq_thresholds = self.thresholds.get("data_quality", {})
            sh_thresholds = self.thresholds.get("source_health", {})

            # Context
            disagreement_diags = cand.metadata.get(
                "source_disagreement_diagnostics", {}
            )
            dq_diags = cand.metadata.get("data_quality_summaries", {})
            selection_diags = cand.metadata.get("source_selection_diagnostics", {})

            # Computations
            edge = compute_edge(cand.final_probability, cand.market_implied_probability)

            entropy = compute_entropy(cand.class_probabilities)
            top_gap = compute_top_class_gap(cand.class_probabilities)
            conf = compute_confidence_score(cand.final_probability, top_gap, entropy)

            uncert = compute_uncertainty_penalty(
                entropy,
                entropy_thresholds,
                unstable_source_set=cand.metadata.get("unstable_source_set", False),
            )

            disagree = compute_disagreement_penalty(
                disagreement_diags, disagreement_thresholds
            )
            dq_penalty = compute_data_quality_penalty(dq_diags, dq_thresholds)
            sh_penalty = compute_source_health_penalty(selection_diags, sh_thresholds)

            comps = SignalComponentRecord(
                edge_estimate=edge,
                confidence_score=conf,
                uncertainty_penalty=uncert,
                disagreement_penalty=disagree,
                data_quality_penalty=dq_penalty,
                source_health_penalty=sh_penalty,
            )

            raw_score = combine_signal_components(comps, self.weights)
            norm_score = normalize_signal_score(raw_score)

            status = SignalStatus.SCORED
            if cand.market_implied_probability is None:
                status = SignalStatus.NO_MARKET_REFERENCE
            elif norm_score < self.thresholds.get(
                "minimum_quality_for_scored_status", 30.0
            ):
                status = SignalStatus.WEAK_SIGNAL

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
