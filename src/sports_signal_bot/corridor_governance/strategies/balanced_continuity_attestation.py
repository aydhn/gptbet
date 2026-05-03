from .base import CorridorGovernanceStrategy

class BalancedContinuityAttestationStrategy(CorridorGovernanceStrategy):
    def get_strategy_name(self) -> str:
        return "BalancedContinuityAttestationStrategy"

    def evaluate_visibility(self) -> str:
        return "balanced"
