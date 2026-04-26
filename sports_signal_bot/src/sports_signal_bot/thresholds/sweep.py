from typing import Any, Dict, List, Optional

import pandas as pd

from sports_signal_bot.evaluation.metrics import compute_all_metrics
from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord

from .constraints import ConstraintEvaluator
from .contracts import (ThresholdCandidateRecord, ThresholdOptimizationResult,
                        ThresholdPolicyRecord, ThresholdSweepRecord)
from .grid import generate_threshold_grid
from .objectives import ObjectiveEvaluator


class ThresholdSweepEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.objective_evaluator = ObjectiveEvaluator(config.get("objective", {}))
        self.constraint_evaluator = ConstraintEvaluator(config.get("constraints", {}))

    def sweep(
        self,
        strategy_name: str,
        signals: List[SignalScoreRecord],
        labels_df: pd.DataFrame,
        sport: str,
        market_type: str,
        true_label_col: str = "target_value",
        class_labels: Optional[List[str]] = None,
    ) -> ThresholdOptimizationResult:
        grid = generate_threshold_grid(self.config.get("grid", {}), strategy_name)

        from .factory import ThresholdStrategyFactory

        strategy = ThresholdStrategyFactory.create(
            strategy_name, self.config.get("strategy_config", {})
        )

        candidates = []
        for params in grid:
            accepted, rejected = strategy.apply_threshold(signals, params)

            cand = ThresholdCandidateRecord(
                market_type=market_type,
                sport=sport,
                score_threshold=params.get("score_threshold", 0.0),
                edge_threshold=params.get("edge_threshold", None),
                accepted_count=len(accepted),
                rejected_count=len(rejected),
                coverage_rate=len(accepted) / max(len(signals), 1),
                acceptance_rate=len(accepted) / max(len(signals), 1),
            )

            if accepted:
                # Merge with labels to compute metrics
                # This requires event_id matching
                accepted_event_ids = [s.event_id for s in accepted]
                eval_df = labels_df[
                    labels_df["event_id"].isin(accepted_event_ids)
                ].copy()

                if not eval_df.empty:
                    # We need to structure the predictions to compute metrics
                    # Create predicted_class and probabilities
                    eval_df["predicted_class"] = [
                        next(s.selection for s in accepted if s.event_id == eid)
                        for eid in eval_df["event_id"]
                    ]

                    # For simplicity, just compute accuracy if we don't have full probas available here easily
                    # In a real implementation, we'd extract the probas properly.
                    # Let's assume we can compute a proxy accuracy
                    if true_label_col in eval_df.columns:
                        y_true = eval_df[true_label_col].values
                        y_pred = eval_df["predicted_class"].values

                        try:
                            from sklearn.metrics import accuracy_score

                            cand.quality_metrics["accuracy"] = float(
                                accuracy_score(y_true, y_pred)
                            )
                        except Exception:
                            cand.quality_metrics["accuracy"] = 0.0

                cand.average_signal_score = sum(
                    s.final_signal_score for s in accepted
                ) / len(accepted)
                cand.average_edge = sum(
                    s.components.edge_estimate for s in accepted
                ) / len(accepted)
                cand.average_confidence = sum(
                    s.components.confidence_score for s in accepted
                ) / len(accepted)
                cand.average_uncertainty_penalty = sum(
                    s.components.uncertainty_penalty for s in accepted
                ) / len(accepted)

            else:
                cand.warnings.append("Empty accepted set")

            cand.objective_value = self.objective_evaluator.evaluate(
                cand, cand.quality_metrics
            )
            candidates.append(cand)

        # Filter and rank
        valid_candidates = []
        for c in candidates:
            if self.constraint_evaluator.check_constraints(c, c.quality_metrics):
                valid_candidates.append(c)

        # Best candidate
        best_candidate = None
        if valid_candidates:
            # Assuming we want to maximize objective
            best_candidate = max(valid_candidates, key=lambda c: c.objective_value)

        return ThresholdOptimizationResult(
            sport=sport,
            market_type=market_type,
            strategy_used=strategy_name,
            best_candidate=best_candidate,
            all_candidates=candidates,
            objective_name=self.objective_evaluator.objective_name,
            constraints_applied=self.config.get("constraints", {}),
            total_evaluated=len(grid),
            warnings=(
                ["No valid candidates after constraints"] if not best_candidate else []
            ),
        )
