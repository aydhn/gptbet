from typing import Any, Dict, List, Tuple

from sports_signal_bot.dynamic_weighting.contracts import (
    DynamicWeightRecord, WeightingDecisionRecord, WeightingDiagnosticsRecord)
from sports_signal_bot.dynamic_weighting.factory import WeightingFactory


class DynamicWeightingRunner:
    def __init__(
        self, strategy_name: str, policy_data: Dict[str, Any], config: Dict[str, Any]
    ):
        self.strategy = WeightingFactory.create(strategy_name, policy_data, config)
        self.strategy_name = strategy_name

    def run(
        self, eligible_sources: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> Tuple[List[DynamicWeightRecord], WeightingDiagnosticsRecord]:
        event_id = context.get("event_id", "unknown")

        # Guard: No eligible sources
        if not eligible_sources:
            return [], WeightingDiagnosticsRecord(event_id=event_id, source_count=0)

        # Guard: Single eligible source
        if len(eligible_sources) == 1:
            # Create a simple fallback record
            source = eligible_sources[0]
            from sports_signal_bot.dynamic_weighting.contracts import \
                WeightComponentRecord

            record = DynamicWeightRecord(
                event_id=event_id,
                sport=context.get("sport", "unknown"),
                market_type=context.get("market_type", "unknown"),
                source_name=source.get("name", "unknown"),
                source_family=source.get("family", "unknown"),
                base_weight=1.0,
                component_scores=WeightComponentRecord(combined_score=1.0),
                pre_normalized_weight=1.0,
                final_weight=1.0,
                weighting_policy_name=self.strategy.policy.name,
                explanation_summary="Single eligible source fallback.",
            )
            diagnostics = WeightingDiagnosticsRecord(
                event_id=event_id,
                source_count=1,
                fallback_used=True,
                top_source=source.get("name", "unknown"),
            )
            return [record], diagnostics

        # Normal flow
        weights = self.strategy.compute_weights(eligible_sources, context)

        # Generate diagnostics
        diagnostics = self._generate_diagnostics(event_id, weights, eligible_sources)

        return weights, diagnostics

    def _generate_diagnostics(
        self,
        event_id: str,
        weights: List[DynamicWeightRecord],
        sources: List[Dict[str, Any]],
    ) -> WeightingDiagnosticsRecord:
        capped = []
        floored = []
        stale = []
        trust_sum = 0.0

        for source in sources:
            trust_sum += source.get("trust_score", 0.0)
            if source.get("is_stale", False):
                stale.append(source.get("name", "unknown"))

        # Find capped/floored from final weights vs pre-normalized
        # A simple heuristic: if final weight == max_cap or == min_floor
        max_cap = self.strategy.policy.max_weight_cap
        min_floor = self.strategy.policy.min_weight_floor

        top_weight = -1.0
        top_source = None

        for w in weights:
            if abs(w.final_weight - max_cap) < 1e-6:
                capped.append(w.source_name)
            if abs(w.final_weight - min_floor) < 1e-6:
                floored.append(w.source_name)

            if w.final_weight > top_weight:
                top_weight = w.final_weight
                top_source = w.source_name

        avg_trust = trust_sum / max(1, len(sources))

        return WeightingDiagnosticsRecord(
            event_id=event_id,
            source_count=len(sources),
            capped_sources=capped,
            floored_sources=floored,
            stale_penalties=stale,
            average_trust=avg_trust,
            top_source=top_source,
        )
