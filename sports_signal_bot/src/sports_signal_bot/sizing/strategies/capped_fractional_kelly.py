from typing import Tuple, List, Optional
from sports_signal_bot.sizing.contracts import StakeSizingInputRecord
from sports_signal_bot.sizing.strategies.fractional_kelly import FractionalKellyOverlay


class CappedFractionalKellyOverlay(FractionalKellyOverlay):
    """
    Computes a Fractional Kelly size, but the RiskLimitEngine will cap it.
    The proposal logic is the same as FractionalKelly, but the intent is that
    it's explicitly designed to hit limits.
    """

    def propose_size(
        self, input_record: StakeSizingInputRecord
    ) -> Tuple[float, Optional[float], List[str]]:
        # Proposal is same as base fractional
        return super().propose_size(input_record)

    def describe(self) -> str:
        return "CappedFractionalKellyOverlay"
