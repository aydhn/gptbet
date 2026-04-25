import datetime
from typing import List

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedEventRegimeClassifier
from sports_signal_bot.regimes.inputs import EventRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_event_classifier("form")
class FormRegimeClassifier(RuleBasedEventRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="form",
            level="event",
            description="Classifies event based on team recent form (win streaks, points)",
            required_inputs=["home_form_score", "away_form_score"],
            assignment_type="rule_based",
        )

    def assign_event_regimes(
        self, inputs: EventRegimeInputs
    ) -> List[EventRegimeRecord]:
        warnings = self.validate_event_inputs(inputs)

        home_form = inputs.features.get("home_form_score", 0.5)
        away_form = inputs.features.get("away_form_score", 0.5)

        if home_form > 0.7 and away_form > 0.7:
            label = "both_hot"
        elif home_form < 0.3 and away_form < 0.3:
            label = "both_cold"
        elif (home_form > 0.7 and away_form < 0.3) or (
            home_form < 0.3 and away_form > 0.7
        ):
            label = "mixed_form"
        elif home_form > 0.7:
            label = "home_team_hot"
        elif away_form > 0.7:
            label = "away_team_hot"
        else:
            label = "stable_form"

        return [
            EventRegimeRecord(
                event_id=inputs.event_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="form",
                regime_label=label,
                assignment_method="rule_based",
                supporting_features={"home_form": home_form, "away_form": away_form},
                warnings=warnings,
            )
        ]
