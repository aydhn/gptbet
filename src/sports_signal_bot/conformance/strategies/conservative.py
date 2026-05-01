from typing import Dict, Any
from .base import BaseConformanceStrategy
from ..contracts import RunMode

class ConservativeConformanceStrategy(BaseConformanceStrategy):
    def apply_strategy(self, state: Dict[str, Any], mode: RunMode) -> Dict[str, Any]:
        # Critical assertions fail-closed, strict exceptions, low drift tolerance
        state["strategy"] = "conservative"
        state["drift_tolerance"] = "low"
        return state
