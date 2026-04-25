from typing import List

import numpy as np

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedEventRegimeClassifier
from sports_signal_bot.regimes.inputs import EventRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_event_classifier("volatility")
class VolatilityRegimeClassifier(RuleBasedEventRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="volatility",
            level="event",
            description="Classifies volatility and uncertainty based on prediction entropy",
            required_inputs=["ensemble_probabilities"],
            assignment_type="rule_based",
        )

    def assign_event_regimes(
        self, inputs: EventRegimeInputs
    ) -> List[EventRegimeRecord]:
        warnings = self.validate_event_inputs(inputs)
        records = []

        probs = list(inputs.ensemble_probabilities.values())
        if not probs:
            warnings.append(
                "No ensemble probabilities provided for entropy calculation"
            )
            records.append(
                EventRegimeRecord(
                    event_id=inputs.event_id,
                    sport=inputs.sport,
                    market_type=inputs.market_type,
                    regime_family="volatility",
                    regime_label="unstable_period",
                    assignment_method="rule_based",
                    supporting_features={},
                    warnings=warnings,
                )
            )
            return records

        # Normalized entropy
        entropy = -sum(p * np.log2(p + 1e-9) for p in probs)
        max_entropy = np.log2(len(probs)) if len(probs) > 0 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        if normalized_entropy > self.config.entropy_thresholds.high:
            label = "high_uncertainty"
            records.append(
                EventRegimeRecord(
                    event_id=inputs.event_id,
                    sport=inputs.sport,
                    market_type=inputs.market_type,
                    regime_family="volatility",
                    regime_label="high_entropy_prediction",
                    regime_value=normalized_entropy,
                    assignment_method="rule_based",
                    supporting_features={"normalized_entropy": normalized_entropy},
                    warnings=[],
                )
            )
        elif normalized_entropy > self.config.entropy_thresholds.high * 0.7:
            label = "medium_uncertainty"
        else:
            label = "low_uncertainty"

        records.append(
            EventRegimeRecord(
                event_id=inputs.event_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="volatility",
                regime_label=label,
                regime_value=normalized_entropy,
                assignment_method="rule_based",
                supporting_features={"normalized_entropy": normalized_entropy},
                warnings=warnings,
            )
        )

        return records
