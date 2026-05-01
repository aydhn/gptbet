from typing import Dict, Any
from .base import BaseConformanceStrategy
from ..contracts import RunMode

class BalancedCompliancePipelineStrategy(BaseConformanceStrategy):
    def apply_strategy(self, state: Dict[str, Any], mode: RunMode) -> Dict[str, Any]:
        # Default balanced, clear warning vs block separation
        state["strategy"] = "balanced"
        state["drift_tolerance"] = "medium"
        return state
