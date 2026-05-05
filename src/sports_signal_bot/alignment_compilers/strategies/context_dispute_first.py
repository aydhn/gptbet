from typing import Dict, Any
from .base import BaseAlignmentCompilerStrategy

class ContextDisputeFirstStrategy(BaseAlignmentCompilerStrategy):
    """
    Context Dispute First Strategy:
    - context integrity, freshness evidence, and trace applicability dominate
    - weak evidence quickly results in review_only/no_safe
    - tribunal caps are highly visible
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ContextDisputeFirstStrategy", config or {})

    def evaluate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        result = {"band": "strong_bounded_alignment", "penalties": [], "caps": []}

        if inputs.get("tribunal_caps_present", False):
            result["band"] = "bounded_alignment_with_caveats"

        if inputs.get("evidence_completeness") != "complete":
            result["band"] = "review_only_alignment"
            result["penalties"].append("weak_evidence_penalty_critical")

        if inputs.get("no_safe_visibility_state") == "hidden":
            result["band"] = "review_only_alignment"
            result["penalties"].append("no_safe_visibility_penalty_critical")

        return result
