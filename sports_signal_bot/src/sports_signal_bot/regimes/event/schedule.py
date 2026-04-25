from typing import List

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedEventRegimeClassifier
from sports_signal_bot.regimes.inputs import EventRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_event_classifier("schedule")
class ScheduleRegimeClassifier(RuleBasedEventRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="schedule",
            level="event",
            description="Classifies schedule/fatigue based on rest days and congestion",
            required_inputs=["home_rest_days", "away_rest_days"],
            assignment_type="rule_based",
        )

    def assign_event_regimes(
        self, inputs: EventRegimeInputs
    ) -> List[EventRegimeRecord]:
        warnings = self.validate_event_inputs(inputs)
        records = []

        home_rest = inputs.features.get("home_rest_days", 7)
        away_rest = inputs.features.get("away_rest_days", 7)

        min_rest = min(home_rest, away_rest)

        if min_rest <= self.config.short_rest_days:
            label = "short_rest"
            if inputs.sport == "basketball" and min_rest <= 1:
                records.append(
                    EventRegimeRecord(
                        event_id=inputs.event_id,
                        sport=inputs.sport,
                        market_type=inputs.market_type,
                        regime_family="schedule",
                        regime_label="basketball_back_to_back",
                        regime_value=float(min_rest),
                        assignment_method="rule_based",
                        supporting_features={
                            "home_rest": home_rest,
                            "away_rest": away_rest,
                        },
                        warnings=[],
                    )
                )
        else:
            label = "normal_rest"

        records.append(
            EventRegimeRecord(
                event_id=inputs.event_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="schedule",
                regime_label=label,
                regime_value=float(min_rest),
                assignment_method="rule_based",
                supporting_features={"home_rest": home_rest, "away_rest": away_rest},
                warnings=warnings,
            )
        )

        home_matches_10d = inputs.features.get("home_matches_last_10d", 1)
        away_matches_10d = inputs.features.get("away_matches_last_10d", 1)
        max_congestion = max(home_matches_10d, away_matches_10d)

        if (
            max_congestion
            >= self.config.congestion_match_count_thresholds.congested_min_matches
        ):
            records.append(
                EventRegimeRecord(
                    event_id=inputs.event_id,
                    sport=inputs.sport,
                    market_type=inputs.market_type,
                    regime_family="schedule",
                    regime_label="congested_schedule",
                    regime_value=float(max_congestion),
                    assignment_method="rule_based",
                    supporting_features={
                        "home_matches_10d": home_matches_10d,
                        "away_matches_10d": away_matches_10d,
                    },
                    warnings=[],
                )
            )
            if inputs.sport == "football":
                records.append(
                    EventRegimeRecord(
                        event_id=inputs.event_id,
                        sport=inputs.sport,
                        market_type=inputs.market_type,
                        regime_family="schedule",
                        regime_label="football_fixture_congestion",
                        regime_value=float(max_congestion),
                        assignment_method="rule_based",
                        supporting_features={
                            "home_matches_10d": home_matches_10d,
                            "away_matches_10d": away_matches_10d,
                        },
                        warnings=[],
                    )
                )

        return records
