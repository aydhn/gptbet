from typing import List
from src.sports_signal_bot.assurance_synthesizers.strategies.base import AssuranceSynthesizerStrategy
from src.sports_signal_bot.assurance_synthesizers.contracts import (
    AssuranceSynthesisInputRecord, AssuranceBand
)

class ConservativeAssuranceSynthesizerStrategy(AssuranceSynthesizerStrategy):
    """
    Stale currentness, freshness gaps, and caveat losses dominate.
    Fast degradation to caveated/stale.
    """
    def evaluate(self, inputs: List[AssuranceSynthesisInputRecord]) -> AssuranceBand:
        for inp in inputs:
            if "deny" in inp.sovereignty_state:
                return AssuranceBand.critically_fragile_assurance
            if "no_safe" in inp.no_safe_visibility_state:
                return AssuranceBand.review_only_assurance
            if "stale" in inp.currentness_state:
                return AssuranceBand.fragile_assurance
        return AssuranceBand.bounded_assurance_with_caveats
