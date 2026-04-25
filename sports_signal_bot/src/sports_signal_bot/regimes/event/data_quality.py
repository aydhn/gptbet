from typing import List

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 RegimeDefinition)
from sports_signal_bot.regimes.definitions import \
    RuleBasedEventRegimeClassifier
from sports_signal_bot.regimes.inputs import EventRegimeInputs
from sports_signal_bot.regimes.registry import RegimeRegistry


@RegimeRegistry.register_event_classifier("data_quality")
class DataQualityRegimeClassifier(RuleBasedEventRegimeClassifier):
    def describe(self) -> RegimeDefinition:
        return RegimeDefinition(
            regime_family="data_quality",
            level="event",
            description="Classifies data quality based on completeness and history size",
            required_inputs=["data_completeness", "missing_sources"],
            assignment_type="rule_based",
        )

    def assign_event_regimes(
        self, inputs: EventRegimeInputs
    ) -> List[EventRegimeRecord]:
        warnings = self.validate_event_inputs(inputs)
        records = []

        missing_ratio = 1.0 - inputs.data_completeness

        if (
            missing_ratio
            <= self.config.data_completeness_thresholds.high_completeness_max_missing
        ):
            label = "high_data_completeness"
        elif (
            missing_ratio
            >= self.config.data_completeness_thresholds.low_completeness_min_missing
        ):
            label = "low_data_completeness"
        else:
            label = "medium_data_completeness"

        records.append(
            EventRegimeRecord(
                event_id=inputs.event_id,
                sport=inputs.sport,
                market_type=inputs.market_type,
                regime_family="data_quality",
                regime_label=label,
                regime_value=inputs.data_completeness,
                assignment_method="rule_based",
                supporting_features={"data_completeness": inputs.data_completeness},
                warnings=warnings,
            )
        )

        if inputs.missing_sources > 0:
            records.append(
                EventRegimeRecord(
                    event_id=inputs.event_id,
                    sport=inputs.sport,
                    market_type=inputs.market_type,
                    regime_family="data_quality",
                    regime_label="missing_key_sources",
                    regime_value=float(inputs.missing_sources),
                    assignment_method="rule_based",
                    supporting_features={"missing_sources": inputs.missing_sources},
                    warnings=[],
                )
            )

        history_count = inputs.features.get("rolling_history_count", 100)
        if (
            history_count
            <= self.config.sparse_history_thresholds.low_history_max_matches
        ):
            records.append(
                EventRegimeRecord(
                    event_id=inputs.event_id,
                    sport=inputs.sport,
                    market_type=inputs.market_type,
                    regime_family="data_quality",
                    regime_label="sparse_history",
                    regime_value=float(history_count),
                    assignment_method="rule_based",
                    supporting_features={"rolling_history_count": history_count},
                    warnings=[],
                )
            )

        return records
