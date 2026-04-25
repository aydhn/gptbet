from typing import List

import numpy as np

from sports_signal_bot.regimes.contracts import (PeriodRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedPeriodRegimeClassifier
from sports_signal_bot.regimes.inputs import PeriodRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_period_classifier("stability")
class StabilityRegimeClassifier(RuleBasedPeriodRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="stability",
            level="period",
            description="Classifies variance across periods",
            required_inputs=["historical_metrics"],
            assignment_type="rule_based",
        )

    def assign_period_regimes(
        self, inputs: PeriodRegimeInputs
    ) -> List[PeriodRegimeRecord]:
        warnings = self.validate_period_inputs(inputs)

        hist = inputs.historical_metrics
        log_losses = [m.get("log_loss") for m in hist if m.get("log_loss") is not None]

        if len(log_losses) < 3:
            return []

        variance = float(np.var(log_losses))

        # Simple hardcoded threshold for example; can be moved to config
        if variance > 0.01:
            label = "high_variance_performance"
        else:
            label = "stable"

        return [
            PeriodRegimeRecord(
                period_id=inputs.period_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="stability",
                regime_label=label,
                assignment_method="rule_based",
                supporting_metrics={"log_loss_variance": variance},
                warnings=warnings,
            )
        ]
