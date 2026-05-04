from .base import BaseAssuranceExchangeStrategy

class DebtSettlementNarrativeFirstStrategy(BaseAssuranceExchangeStrategy):
    @property
    def name(self) -> str:
        return "DebtSettlementNarrativeFirstStrategy"

    def apply_currentness_rules(self, snapshot_age: int) -> str:
        if snapshot_age > 3600:
            return "snapshot_stale"
        return "snapshot_current"

    def apply_board_clearing_rules(self) -> str:
        return "cleared_review_only_replay"
