from .base import BaseFinalConvergenceStrategy
from typing import Dict, Any

class AcceptanceHonestyFirstStrategy(BaseFinalConvergenceStrategy):
    def evaluate(self, convergence_data: Dict[str, Any]) -> bool:
        # acceptance evidence sufficiency, replayability and residue honesty dominant

        acceptance = convergence_data.get("acceptance")
        if not acceptance: return False

        if not acceptance.evidence_refs:
            return False

        if not all(e.replayable for e in acceptance.evidence_refs):
            return False

        if any(r.hidden for r in acceptance.residue_refs):
            return False

        return True
