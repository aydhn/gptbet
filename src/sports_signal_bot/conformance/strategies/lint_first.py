from typing import Dict, Any
from .base import BaseConformanceStrategy
from ..contracts import RunMode

class LintFirstGovernanceStrategy(BaseConformanceStrategy):
    def apply_strategy(self, state: Dict[str, Any], mode: RunMode) -> Dict[str, Any]:
        # Heavy early lint discipline
        state["strategy"] = "lint_first"
        state["lint_strictness"] = "high"
        return state
