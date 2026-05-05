from typing import List
from src.sports_signal_bot.assurance_synthesizers.strategies.base import AssuranceSynthesizerStrategy
from src.sports_signal_bot.assurance_synthesizers.contracts import (
    AssuranceSynthesisInputRecord, AssuranceBand
)

class BalancedCouncilClearingSynthesisStrategy(AssuranceSynthesizerStrategy):
    """
    Balanced approach. Useful bounded assurance but safety-first.
    """
    def evaluate(self, inputs: List[AssuranceSynthesisInputRecord]) -> AssuranceBand:
        band = AssuranceBand.strong_bounded_assurance
        for inp in inputs:
            if "deny" in inp.sovereignty_state:
                return AssuranceBand.critically_fragile_assurance
            if "no_safe" in inp.no_safe_visibility_state:
                if band in (AssuranceBand.strong_bounded_assurance, AssuranceBand.stabilized_assurance_with_caps):
                    band = AssuranceBand.review_only_assurance
            elif "stale" in inp.currentness_state:
                if band == AssuranceBand.strong_bounded_assurance:
                    band = AssuranceBand.bounded_assurance_with_caveats
        return band
