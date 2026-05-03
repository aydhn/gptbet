from .base import CorridorGovernanceStrategy

class ScorecardStrictStrategy(CorridorGovernanceStrategy):
    def get_strategy_name(self) -> str:
        return "ScorecardStrictStrategy"

    def evaluate_visibility(self) -> str:
        return "score_based"
