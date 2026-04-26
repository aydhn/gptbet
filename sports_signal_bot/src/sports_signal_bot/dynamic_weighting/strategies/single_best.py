from typing import Any, Dict, List

from sports_signal_bot.dynamic_weighting.components import \
    combine_weight_components
from sports_signal_bot.dynamic_weighting.contracts import DynamicWeightRecord
from sports_signal_bot.dynamic_weighting.normalization import \
    explain_weighting_decision
from sports_signal_bot.dynamic_weighting.strategies.base import \
    BaseWeightingStrategy


class SingleBestSourceWeighted(BaseWeightingStrategy):
    def compute_weights(
        self, eligible_sources: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> List[DynamicWeightRecord]:
        if not self.validate_inputs(eligible_sources):
            return []

        event_id = context.get("event_id", "unknown")
        sport = context.get("sport", "unknown")
        market_type = context.get("market_type", "unknown")

        records = []

        # Find best source by trust score
        best_source = max(eligible_sources, key=lambda s: s.get("trust_score", 0.0))
        best_source_name = best_source.get("name", "unknown")

        for source in eligible_sources:
            source_name = source.get("name", "unknown")
            source_family = source.get("family", "unknown")

            trust_val = source.get("trust_score", 0.5)

            components = combine_weight_components(
                trust=trust_val,
                regime=0.0,
                disagreement=0.0,
                recency=0.0,
                health=1.0,
                prior=1.0,
                bonus=0.0,
                policy=self.policy,
            )

            final_weight = 1.0 if source_name == best_source_name else 0.0

            record = DynamicWeightRecord(
                event_id=event_id,
                sport=sport,
                market_type=market_type,
                source_name=source_name,
                source_family=source_family,
                base_weight=1.0,
                component_scores=components,
                pre_normalized_weight=trust_val,
                final_weight=final_weight,
                weighting_policy_name=self.policy.name,
            )
            record.explanation_summary = explain_weighting_decision(
                record.source_name, record.final_weight, record.component_scores
            )
            records.append(record)

        return records
