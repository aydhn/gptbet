from typing import Tuple, List
from sports_signal_bot.bankroll.contracts import BankrollDecisionRecord
from sports_signal_bot.bankroll.overlays.base import BaseOverlayStrategy

class ConservativeCappedFractionOverlay(BaseOverlayStrategy):
    def compute_stake(self, decision: BankrollDecisionRecord, current_bankroll: float) -> Tuple[float, List[str]]:
        warnings = []
        # Uses bankroll_fraction, but subject to strict min/max limits
        stake = current_bankroll * self.config.bankroll_fraction

        # apply_stake_caps in runner will handle the actual limits,
        # but here we can add extra conservative logic if needed.
        # For now, it delegates to the base limits.

        return stake, warnings
