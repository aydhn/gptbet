from typing import List

import numpy as np

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedEventRegimeClassifier
from sports_signal_bot.regimes.inputs import EventRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_event_classifier("market_disagreement")
class MarketDisagreementRegimeClassifier(RuleBasedEventRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="market_disagreement",
            level="event",
            description="Classifies source disagreement based on probability dispersion",
            required_inputs=["source_probabilities"],
            assignment_type="rule_based",
        )

    def assign_event_regimes(
        self, inputs: EventRegimeInputs
    ) -> List[EventRegimeRecord]:
        warnings = self.validate_event_inputs(inputs)
        records = []

        # Calculate disagreement (standard deviation of probabilities across sources for the favorite)
        probs = inputs.source_probabilities
        if not probs:
            warnings.append("No source probabilities provided")
            label = "line_uncertain"
            value = 0.0

            records.append(
                EventRegimeRecord(
                    event_id=inputs.event_id,
                    sport=inputs.sport,
                    market_type=inputs.market_type,
                    regime_family="market_disagreement",
                    regime_label=label,
                    assignment_method="rule_based",
                    supporting_features={},
                    warnings=warnings,
                )
            )
            return records

        # Simple dispersion metric: max std dev across any class
        classes = list(probs.values())[0].keys() if probs else []
        if not classes:
            warnings.append("No probability classes found")
            return []

        std_devs = []
        for cls in classes:
            class_probs = [source_dict.get(cls, 0.0) for source_dict in probs.values()]
            if len(class_probs) > 1:
                std_devs.append(float(np.std(class_probs)))
            else:
                std_devs.append(0.0)

        max_dispersion = max(std_devs) if std_devs else 0.0

        if max_dispersion > self.config.disagreement_thresholds.high:
            label = "high_source_disagreement"
        elif max_dispersion > self.config.disagreement_thresholds.low:
            label = "medium_source_disagreement"
        else:
            label = "low_source_disagreement"

        records.append(
            EventRegimeRecord(
                event_id=inputs.event_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="market_disagreement",
                regime_label=label,
                regime_value=max_dispersion,
                assignment_method="rule_based",
                supporting_features={"max_dispersion": max_dispersion},
                warnings=warnings,
            )
        )

        # Favorite clear regime
        if inputs.ensemble_probabilities:
            max_prob = max(inputs.ensemble_probabilities.values())
            if max_prob > self.config.favorite_prob_thresholds.clear_favorite:
                records.append(
                    EventRegimeRecord(
                        event_id=inputs.event_id,
                        sport=inputs.sport,
                        market_type=inputs.market_type,
                        regime_family="market_disagreement",
                        regime_label="favorite_clear",
                        regime_value=max_prob,
                        assignment_method="rule_based",
                        supporting_features={"implied_favorite_prob": max_prob},
                        warnings=[],
                    )
                )
            else:
                sorted_probs = sorted(
                    inputs.ensemble_probabilities.values(), reverse=True
                )
                if (
                    len(sorted_probs) > 1
                    and (sorted_probs[0] - sorted_probs[1])
                    < self.config.favorite_prob_thresholds.market_close_diff
                ):
                    records.append(
                        EventRegimeRecord(
                            event_id=inputs.event_id,
                            sport=inputs.sport,
                            market_type=inputs.market_type,
                            regime_family="market_disagreement",
                            regime_label="market_close",
                            regime_value=sorted_probs[0] - sorted_probs[1],
                            assignment_method="rule_based",
                            supporting_features={
                                "top_two_diff": sorted_probs[0] - sorted_probs[1]
                            },
                            warnings=[],
                        )
                    )

        return records
