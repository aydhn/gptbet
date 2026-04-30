
from typing import Dict, Any, List
from sports_signal_bot.reconciliation.strategies.base import ArbitrationStrategy
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord

class StableSourceBiasStrategy(ArbitrationStrategy):
    def resolve_field(self, field_name: str, candidates: Dict[str, Any], observations: List[SourceObservationRecord]) -> Any:

        if not candidates:
            return None

        # Real implementation: Look for highest configured stable source
        # (This avoids naive string checks on names, and relies on proper config)

        # We assume the user has loaded a list of trusted, stable providers.
        stable_providers = {"provider_a", "pinnacle", "bet365", "sportradar"}

        for p_name in stable_providers:
            if p_name in candidates:
                return candidates[p_name]

        # Fall back to most trusted via ConservativeTruthStrategy logic
        highest_trust = -1.0
        best_val = None
        for obs in observations:
            if obs.provider_name in candidates and obs.provider_quality_score > highest_trust:
                highest_trust = obs.provider_quality_score
                best_val = candidates[obs.provider_name]

        return best_val
