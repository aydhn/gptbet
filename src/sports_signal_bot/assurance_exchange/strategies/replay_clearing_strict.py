from .base import BaseAssuranceExchangeStrategy

class ReplayClearingStrictStrategy(BaseAssuranceExchangeStrategy):
    @property
    def name(self) -> str:
        return "ReplayClearingStrictStrategy"

    def apply_currentness_rules(self, snapshot_age: int) -> str:
        if snapshot_age > 1800:
            return "snapshot_stale"
        return "snapshot_current"

    def apply_board_clearing_rules(self) -> str:
        return "cleared_blocked_no_safe_path"
