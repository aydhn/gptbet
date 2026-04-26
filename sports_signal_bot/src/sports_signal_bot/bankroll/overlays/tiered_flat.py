from typing import Tuple, List
from sports_signal_bot.bankroll.contracts import BankrollDecisionRecord
from sports_signal_bot.bankroll.overlays.base import BaseOverlayStrategy

class SignalTieredFlatOverlay(BaseOverlayStrategy):
    def compute_stake(self, decision: BankrollDecisionRecord, current_bankroll: float) -> Tuple[float, List[str]]:
        warnings = []
        # approved_candidate gets flat, candidate gets half, watchlist gets 0
        action = decision.action_class.lower()
        if "approved_candidate" in action or action == "approved":
            return self.config.flat_stake_units, warnings
        elif "candidate" in action:
            return self.config.flat_stake_units * 0.5, warnings
        elif "watchlist" in action or "no_action" in action:
            return 0.0, warnings

        warnings.append(f"Tiered flat: Unrecognized action class {action}, using default flat.")
        return self.config.flat_stake_units, warnings
