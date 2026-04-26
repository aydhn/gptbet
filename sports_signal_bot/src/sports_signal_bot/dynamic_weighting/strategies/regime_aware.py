from typing import Any, Dict, List

from sports_signal_bot.dynamic_weighting.components import (
    combine_weight_components, compute_base_prior,
    compute_regime_weight_component, compute_trust_weight_component)
from sports_signal_bot.dynamic_weighting.contracts import DynamicWeightRecord
from sports_signal_bot.dynamic_weighting.normalization import (
    explain_weighting_decision, normalize_weights)
from sports_signal_bot.dynamic_weighting.strategies.base import \
    BaseWeightingStrategy


class RegimeAwareWeighted(BaseWeightingStrategy):
    def compute_weights(
        self, eligible_sources: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> List[DynamicWeightRecord]:
        if not self.validate_inputs(eligible_sources):
            return []

        event_id = context.get("event_id", "unknown")
        sport = context.get("sport", "unknown")
        market_type = context.get("market_type", "unknown")

        records = []
        combined_scores = []

        for source in eligible_sources:
            source_name = source.get("name", "unknown")
            source_family = source.get("family", "unknown")

            prior = compute_base_prior(
                source_family, market_type, self.config.get("family_priors", {})
            )

            trust_val = source.get("trust_score", 0.5)
            trust = compute_trust_weight_component(trust_val)

            regime_val = source.get("regime_fit", 0.0)
            sample_size = source.get("regime_sample_size", 0)
            regime = compute_regime_weight_component(
                regime_val, sample_size, self.policy.regime_sample_damping
            )

            # Simple policy: trust + prior + regime
            components = combine_weight_components(
                trust=trust,
                regime=regime,
                disagreement=0.0,
                recency=0.0,
                health=1.0,
                prior=prior,
                bonus=0.0,
                policy=self.policy,
            )

            combined_scores.append(components.combined_score)

            record = DynamicWeightRecord(
                event_id=event_id,
                sport=sport,
                market_type=market_type,
                source_name=source_name,
                source_family=source_family,
                base_weight=prior,
                component_scores=components,
                pre_normalized_weight=components.combined_score,
                weighting_policy_name=self.policy.name,
            )
            records.append(record)

        final_weights = normalize_weights(
            combined_scores,
            temperature=self.policy.score_temperature,
            min_floor=self.policy.min_weight_floor,
            max_cap=self.policy.max_weight_cap,
        )

        for i, record in enumerate(records):
            record.final_weight = final_weights[i]
            record.explanation_summary = explain_weighting_decision(
                record.source_name, record.final_weight, record.component_scores
            )

        return records
