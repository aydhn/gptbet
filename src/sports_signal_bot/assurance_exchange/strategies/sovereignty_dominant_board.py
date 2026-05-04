from .base import BaseAssuranceExchangeStrategy

class SovereigntyDominantBoardStrategy(BaseAssuranceExchangeStrategy):
    @property
    def name(self) -> str:
        return "SovereigntyDominantBoardStrategy"

    def apply_currentness_rules(self, snapshot_age: int) -> str:
        if snapshot_age > 1800:
            return "snapshot_stale"
        return "snapshot_current"

    def apply_board_clearing_rules(self) -> str:
        return "cleared_caveated_replay"
