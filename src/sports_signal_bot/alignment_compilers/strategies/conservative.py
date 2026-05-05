from typing import Dict, Any
from .base import BaseAlignmentCompilerStrategy

class ConservativeAlignmentCompilerStrategy(BaseAlignmentCompilerStrategy):
    """
    Conservative Strategy:
    - stale currentness, freshness gaps, and caveat losses are heavily penalized
    - federations, exchange routes, and context bundles quickly become caveated/stale
    - no-safe visibility is of highest importance
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ConservativeAlignmentCompilerStrategy", config or {})

    def evaluate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        result = {"band": "strong_bounded_alignment", "penalties": [], "caps": []}

        # Heavy penalty for staleness
        if inputs.get("currentness_state") == "stale":
            result["band"] = "review_only_alignment"
            result["penalties"].append("stale_context_penalty_critical")

        # Heavy penalty for freshness gaps or incomplete evidence
        if inputs.get("evidence_completeness") != "complete":
            if result["band"] == "strong_bounded_alignment":
                result["band"] = "bounded_alignment_with_caveats"
            result["penalties"].append("evidence_gap_penalty_high")

        # No-safe visibility must be preserved
        if inputs.get("no_safe_visibility_state") == "hidden":
            result["band"] = "review_only_alignment"
            result["penalties"].append("no_safe_visibility_penalty_critical")

        return result
