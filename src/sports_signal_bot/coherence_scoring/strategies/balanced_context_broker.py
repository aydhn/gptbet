from typing import Dict, Any, List
from .base import CoherenceScoringStrategy
from ..coherence_scorers import STABILIZED_COHERENCE_WITH_CAPS, REVIEW_ONLY_COHERENCE

class BalancedContextBrokerStrategy(CoherenceScoringStrategy):
    def evaluate(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        band = STABILIZED_COHERENCE_WITH_CAPS
        stale_count = sum(1 for inp in inputs if inp.get("currentness_state") == "stale")
        if stale_count > 0:
            band = REVIEW_ONLY_COHERENCE
        return {"band": band, "explanation": "Balanced context broker strategy applied."}
