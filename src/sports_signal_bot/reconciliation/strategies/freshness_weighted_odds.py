
from typing import Dict, Any, List
from sports_signal_bot.reconciliation.strategies.base import ArbitrationStrategy
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord

class FreshnessWeightedOddsStrategy(ArbitrationStrategy):
    def resolve_field(self, field_name: str, candidates: Dict[str, Any], observations: List[SourceObservationRecord]) -> Any:

        if not candidates:
            return None

        # Freshness + Trust Threshold Logic
        TRUST_THRESHOLD = 0.5

        freshest_time = None
        best_val = None

        for obs in observations:
            if obs.provider_name in candidates:
                if obs.provider_quality_score < TRUST_THRESHOLD:
                    continue  # Ignore untrusted sources regardless of freshness

                if freshest_time is None or obs.source_snapshot_time > freshest_time:
                    freshest_time = obs.source_snapshot_time
                    best_val = candidates[obs.provider_name]

        if best_val is None:
            # Fallback if no source meets trust threshold
            return list(candidates.values())[0]

        return best_val
