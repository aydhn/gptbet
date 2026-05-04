from .base import BaseAssuranceExchangeStrategy

class BalancedBoardClearingStrategy(BaseAssuranceExchangeStrategy):
    @property
    def name(self) -> str:
        return "BalancedBoardClearingStrategy"

    def apply_currentness_rules(self, snapshot_age: int) -> str:
        if snapshot_age > 3600: # 1 hr
            return "snapshot_stale"
        elif snapshot_age > 1800:
            return "snapshot_caveated"
        return "snapshot_current"

    def apply_board_clearing_rules(self) -> str:
        return "cleared_bounded_replay"
