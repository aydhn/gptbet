from typing import Tuple, List
from sports_signal_bot.bankroll.contracts import BankrollDecisionRecord
from sports_signal_bot.bankroll.overlays.base import BaseOverlayStrategy

class FlatStakeOverlay(BaseOverlayStrategy):
    def compute_stake(self, decision: BankrollDecisionRecord, current_bankroll: float) -> Tuple[float, List[str]]:
        return self.config.flat_stake_units, []
