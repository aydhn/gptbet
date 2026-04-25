from typing import List

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedEventRegimeClassifier
from sports_signal_bot.regimes.inputs import EventRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_event_classifier("season")
class SeasonRegimeClassifier(RuleBasedEventRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="season",
            level="event",
            description="Classifies season phase based on progression",
            required_inputs=["season_progress"],
            assignment_type="rule_based",
        )

    def assign_event_regimes(
        self, inputs: EventRegimeInputs
    ) -> List[EventRegimeRecord]:
        warnings = self.validate_event_inputs(inputs)

        progress = inputs.features.get("season_progress", 0.5)

        if progress <= self.config.season_progress_buckets.early_max:
            label = "season_early"
        elif progress >= self.config.season_progress_buckets.late_min:
            label = "season_late"
        else:
            label = "season_mid"

        return [
            EventRegimeRecord(
                event_id=inputs.event_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="season",
                regime_label=label,
                regime_value=progress,
                assignment_method="rule_based",
                supporting_features={"season_progress": progress},
                warnings=warnings,
            )
        ]
