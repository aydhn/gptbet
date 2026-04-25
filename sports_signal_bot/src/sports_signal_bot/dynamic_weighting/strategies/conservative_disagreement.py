from typing import List, Dict, Any
from sports_signal_bot.dynamic_weighting.contracts import DynamicWeightRecord
from sports_signal_bot.dynamic_weighting.strategies.base import BaseWeightingStrategy
from sports_signal_bot.dynamic_weighting.components import compute_trust_weight_component, compute_disagreement_component, combine_weight_components
from sports_signal_bot.dynamic_weighting.normalization import normalize_weights, explain_weighting_decision

class ConservativeDisagreementWeighted(BaseWeightingStrategy):
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

            trust_val = source.get('trust_score', 0.5)
            trust = compute_trust_weight_component(trust_val)

            prob = source.get('probability', 0.5)
            disagreement = compute_disagreement_component(
                prob, peer_probs,
                self.policy.minimum_peer_count_for_disagreement,
                self.policy.disagreement_penalty_weight
            )

            # Simple policy: trust + disagreement
            components = combine_weight_components(
                trust=trust, regime=0.0, disagreement=disagreement, recency=0.0, health=1.0,
                prior=1.0, bonus=0.0, policy=self.policy
            )

            combined_scores.append(components.combined_score)

            record = DynamicWeightRecord(
                event_id=event_id,
                sport=sport,
                market_type=market_type,
                source_name=source_name,
                source_family=source_family,
                base_weight=1.0,
                component_scores=components,
                pre_normalized_weight=components.combined_score,
                weighting_policy_name=self.policy.name
            )
            records.append(record)

        final_weights = normalize_weights(
            combined_scores,
            temperature=self.policy.score_temperature,
            min_floor=self.policy.min_weight_floor,
            max_cap=self.policy.max_weight_cap
        )

        for i, record in enumerate(records):
            record.final_weight = final_weights[i]
            record.explanation_summary = explain_weighting_decision(record.source_name, record.final_weight, record.component_scores)

        return records
