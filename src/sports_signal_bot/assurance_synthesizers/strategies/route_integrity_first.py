from typing import List
from src.sports_signal_bot.assurance_synthesizers.strategies.base import AssuranceSynthesizerStrategy
from src.sports_signal_bot.assurance_synthesizers.contracts import (
    AssuranceSynthesisInputRecord, AssuranceBand
)

class RouteIntegrityFirstStrategy(AssuranceSynthesizerStrategy):
    """
    Context integrity and trace applicability dominant. Weak evidence fast degrades.
    """
    def evaluate(self, inputs: List[AssuranceSynthesisInputRecord]) -> AssuranceBand:
        for inp in inputs:
            if "deny" in inp.sovereignty_state:
                return AssuranceBand.critically_fragile_assurance
            if "stale" in inp.currentness_state or "no_safe" in inp.no_safe_visibility_state:
                return AssuranceBand.review_only_assurance
        return AssuranceBand.stabilized_assurance_with_caps
