from typing import List

from sports_signal_bot.regimes.contracts import (PeriodRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedPeriodRegimeClassifier
from sports_signal_bot.regimes.inputs import PeriodRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_period_classifier("benchmark_relation")
class BenchmarkRelationRegimeClassifier(RuleBasedPeriodRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="benchmark_relation",
            level="period",
            description="Classifies performance against benchmark",
            required_inputs=["evaluation_summary"],
            assignment_type="rule_based",
        )

    def assign_period_regimes(
        self, inputs: PeriodRegimeInputs
    ) -> List[PeriodRegimeRecord]:
        warnings = self.validate_period_inputs(inputs)

        # evaluation_summary should have a "benchmark_delta" or something
        delta = inputs.evaluation_summary.get("benchmark_delta", 0.0)

        if delta < -0.01:  # Model is worse than benchmark
            label = "underperforming_benchmark"
        elif delta > 0.01:  # Model is better
            label = "outperforming_benchmark"
        else:
            label = "stable"

        return [
            PeriodRegimeRecord(
                period_id=inputs.period_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="benchmark_relation",
                regime_label=label,
                assignment_method="rule_based",
                supporting_metrics={"benchmark_delta": delta},
                warnings=warnings,
            )
        ]
