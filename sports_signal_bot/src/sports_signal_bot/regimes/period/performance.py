from typing import List

import numpy as np

from sports_signal_bot.regimes.contracts import (PeriodRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedPeriodRegimeClassifier
from sports_signal_bot.regimes.inputs import PeriodRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_period_classifier("performance")
class PerformanceRegimeClassifier(RuleBasedPeriodRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="performance",
            level="period",
            description="Classifies period performance trend (degrading, recovering, stable)",
            required_inputs=["historical_metrics"],
            assignment_type="rule_based",
        )

    def assign_period_regimes(
        self, inputs: PeriodRegimeInputs
    ) -> List[PeriodRegimeRecord]:
        warnings = self.validate_period_inputs(inputs)

        hist = inputs.historical_metrics
        if len(hist) < 2:
            warnings.append("Not enough history for performance trend")
            return [
                PeriodRegimeRecord(
                    period_id=inputs.period_id,
                    sport=inputs.sport,
                    market_type=inputs.market_type,
                    regime_family="performance",
                    regime_label="stable",
                    assignment_method="rule_based",
                    supporting_metrics={},
                    warnings=warnings,
                )
            ]

        # Example using log loss, assuming smaller is better
        # We need historical metrics to have "log_loss"
        log_losses = [m.get("log_loss") for m in hist if m.get("log_loss") is not None]

        if len(log_losses) < 2:
            return [
                PeriodRegimeRecord(
                    period_id=inputs.period_id,
                    sport=inputs.sport,
                    market_type=inputs.market_type,
                    regime_family="performance",
                    regime_label="stable",
                    assignment_method="rule_based",
                    supporting_metrics={},
                    warnings=["No valid log_loss found in history"],
                )
            ]

        recent = log_losses[-1]
        previous = log_losses[-2]

        delta = recent - previous  # positive delta means log loss increased (degrading)

        if delta >= self.config.performance_degradation_thresholds.degrading_min_delta:
            label = "degrading"
        elif (
            delta <= self.config.performance_degradation_thresholds.recovering_min_delta
        ):
            label = "recovering"
        else:
            label = "stable"

        return [
            PeriodRegimeRecord(
                period_id=inputs.period_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="performance",
                regime_label=label,
                assignment_method="rule_based",
                supporting_metrics={
                    "delta_log_loss": delta,
                    "recent": recent,
                    "previous": previous,
                },
                warnings=warnings,
            )
        ]
