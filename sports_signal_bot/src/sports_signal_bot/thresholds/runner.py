import json
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord

from .contracts import (SelectivePredictionRecord, ThresholdCandidateRecord,
                        ThresholdManifest, ThresholdOptimizationResult,
                        ThresholdPolicyRecord)
from .factory import ThresholdStrategyFactory
from .frontier import ThresholdFrontierBuilder
from .sweep import ThresholdSweepEngine


class ThresholdRunner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sweep_engine = ThresholdSweepEngine(config.get("sweep_engine", {}))

    def optimize(
        self,
        strategy_name: str,
        signals: List[SignalScoreRecord],
        labels_df: pd.DataFrame,
        sport: str,
        market_type: str,
    ) -> ThresholdOptimizationResult:

        return self.sweep_engine.sweep(
            strategy_name, signals, labels_df, sport, market_type
        )

    def apply_policy(
        self, policy: ThresholdPolicyRecord, signals: List[SignalScoreRecord]
    ) -> List[SelectivePredictionRecord]:

        strategy = ThresholdStrategyFactory.create(policy.signal_strategy, {})
        params = {"score_threshold": policy.selected_threshold}
        if policy.edge_threshold is not None:
            params["edge_threshold"] = policy.edge_threshold

        accepted, rejected = strategy.apply_threshold(signals, params)

        results = []
        for s in accepted:
            results.append(
                SelectivePredictionRecord(
                    event_id=s.event_id,
                    sport=s.sport,
                    market_type=s.market_type,
                    selection=s.selection,
                    is_accepted=True,
                    rejection_reason=None,
                    final_signal_score=s.final_signal_score,
                    edge_estimate=s.components.edge_estimate,
                    policy_used=policy.policy_name,
                    threshold_values=params,
                    component_snapshots={
                        "confidence": s.components.confidence_score,
                        "uncertainty": s.components.uncertainty_penalty,
                    },
                )
            )

        for s in rejected:
            results.append(
                SelectivePredictionRecord(
                    event_id=s.event_id,
                    sport=s.sport,
                    market_type=s.market_type,
                    selection=s.selection,
                    is_accepted=False,
                    rejection_reason="below_threshold",  # Simplify for now
                    final_signal_score=s.final_signal_score,
                    edge_estimate=s.components.edge_estimate,
                    policy_used=policy.policy_name,
                    threshold_values=params,
                    component_snapshots={
                        "confidence": s.components.confidence_score,
                        "uncertainty": s.components.uncertainty_penalty,
                    },
                )
            )

        return results
