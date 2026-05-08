from .base import BaseFinalConvergenceStrategy
from typing import Dict, Any

class ConservativeFinalConvergenceStrategy(BaseFinalConvergenceStrategy):
    def evaluate(self, convergence_data: Dict[str, Any]) -> bool:
        # slightest blocker carry-over, stale baseline or acceptance gap visible -> False
        # stale support rejection strict -> False

        matrix = convergence_data.get("matrix", {})
        if not matrix: return False

        for k, v in matrix.items():
            if not v.get("verified", False):
                return False
            if not v.get("blocker_truth_explicit", False):
                return False
            if v.get("residue_visible", False): # Very conservative, no residue allowed
                pass

        # Must have no stale inputs
        convergence = convergence_data.get("convergence")
        if convergence and any(i.is_stale for i in convergence.input_refs):
            return False

        return True
