
from typing import Dict, Any, List
from sports_signal_bot.reconciliation.strategies.base import ArbitrationStrategy
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord

class ConservativeTruthStrategy(ArbitrationStrategy):
    def resolve_field(self, field_name: str, candidates: Dict[str, Any], observations: List[SourceObservationRecord]) -> Any:
        if not candidates:
            return None

        # Find highest trust source
        highest_trust = -1.0
        best_val = None

        for obs in observations:
            if obs.provider_name in candidates:
                if obs.provider_quality_score > highest_trust:
                    highest_trust = obs.provider_quality_score
                    best_val = candidates[obs.provider_name]

        return best_val
