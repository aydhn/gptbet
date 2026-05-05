from typing import Dict, Any, List
from .base import CoherenceScoringStrategy
from ..coherence_scorers import REVIEW_ONLY_COHERENCE, BOUNDED_COHERENCE_WITH_CAVEATS

class FreshnessDisputeFirstStrategy(CoherenceScoringStrategy):
    def evaluate(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        band = BOUNDED_COHERENCE_WITH_CAVEATS
        for inp in inputs:
            if inp.get("freshness_gap"):
                band = REVIEW_ONLY_COHERENCE
                break
        return {"band": band, "explanation": "Freshness dispute first strategy applied."}
