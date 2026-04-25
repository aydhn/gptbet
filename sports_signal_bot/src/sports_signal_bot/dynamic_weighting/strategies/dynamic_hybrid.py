from typing import List, Dict, Any
from sports_signal_bot.dynamic_weighting.contracts import DynamicWeightRecord
from sports_signal_bot.dynamic_weighting.strategies.base import BaseWeightingStrategy
from sports_signal_bot.dynamic_weighting.components import (
    compute_base_prior, compute_trust_weight_component,
    compute_regime_weight_component, compute_disagreement_component,
    compute_recency_component, combine_weight_components
)
from sports_signal_bot.dynamic_weighting.normalization import normalize_weights, explain_weighting_decision

class DynamicHybridWeighted(BaseWeightingStrategy):
    def compute_weights(self, eligible_sources: List[Dict[str, Any]], context: Dict[str, Any]) -> List[DynamicWeightRecord]:
        if not self.validate_inputs(eligible_sources):
            return []

        event_id = context.get('event_id', 'unknown')
        sport = context.get('sport', 'unknown')
        market_type = context.get('market_type', 'unknown')

        # Gather peer probabilities for disagreement
        peer_probs = [s.get('probability', 0.5) for s in eligible_sources if 'probability' in s]

        records = []
        combined_scores = []

        for source in eligible_sources:
            source_name = source.get('name', 'unknown')
            source_family = source.get('family', 'unknown')

            prior = compute_base_prior(source_family, market_type, self.config.get('family_priors', {}))

            trust_val = source.get('trust_score', 0.5)
            trust = compute_trust_weight_component(trust_val)

            regime_val = source.get('regime_fit', 0.0)
            sample_size = source.get('regime_sample_size', 0)
            regime = compute_regime_weight_component(regime_val, sample_size, self.policy.regime_sample_damping)

            prob = source.get('probability', 0.5)
            disagreement = compute_disagreement_component(
                prob, peer_probs,
                self.policy.minimum_peer_count_for_disagreement,
                self.policy.disagreement_penalty_weight
            )

            is_stale = source.get('is_stale', False)
            recency = compute_recency_component(is_stale, self.policy.recency_penalty_weight)

            health = source.get('health_score', 1.0)
            is_calibrated = source.get('is_calibrated', False)
            bonus = self.policy.calibrated_bonus if is_calibrated else 0.0

            components = combine_weight_components(
                trust, regime, disagreement, recency, health, prior, bonus, self.policy
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
                weighting_policy_name=self.policy.name
            )
            records.append(record)

        # Normalize weights
        final_weights = normalize_weights(
            combined_scores,
            temperature=self.policy.score_temperature,
            min_floor=self.policy.min_weight_floor,
            max_cap=self.policy.max_weight_cap
        )

        # Apply final weights and generate explanations
        for i, record in enumerate(records):
            record.final_weight = final_weights[i]
            record.explanation_summary = explain_weighting_decision(record.source_name, record.final_weight, record.component_scores)

        return records
