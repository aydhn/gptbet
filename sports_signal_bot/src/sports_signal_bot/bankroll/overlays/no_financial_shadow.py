from typing import Tuple, List
from sports_signal_bot.bankroll.contracts import BankrollDecisionRecord
from sports_signal_bot.bankroll.overlays.base import BaseOverlayStrategy

class NoFinancialShadowOverlay(BaseOverlayStrategy):
    def compute_stake(self, decision: BankrollDecisionRecord, current_bankroll: float) -> Tuple[float, List[str]]:
        return 0.0, ["No financial shadow mode active."]
