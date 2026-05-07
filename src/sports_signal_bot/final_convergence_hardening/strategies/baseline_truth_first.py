from .base import BaseFinalConvergenceStrategy
from typing import Dict, Any

class BaselineTruthFirstStrategy(BaseFinalConvergenceStrategy):
    def evaluate(self, convergence_data: Dict[str, Any]) -> bool:
        # frozen baseline scope honesty, drift visibility and freshness dominant
        # hidden baseline erosion intolerable

        baseline = convergence_data.get("baseline")
        if not baseline: return False

        if any(d.hidden for d in baseline.drift_refs):
            return False

        if any(f.is_stale for f in baseline.freshness_refs):
            return False

        return True
