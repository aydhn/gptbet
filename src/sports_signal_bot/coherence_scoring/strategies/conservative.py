from typing import Dict, Any, List
from .base import CoherenceScoringStrategy
from ..coherence_scorers import CRITICALLY_FRAGILE, BOUNDED_COHERENCE_WITH_CAVEATS

class ConservativeCoherenceScoringStrategy(CoherenceScoringStrategy):
    def evaluate(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        band = BOUNDED_COHERENCE_WITH_CAVEATS
        for inp in inputs:
            if inp.get("currentness_state") == "stale" or inp.get("sovereignty_state") == "failed":
                band = CRITICALLY_FRAGILE
        return {"band": band, "explanation": "Conservative strategy applied."}
