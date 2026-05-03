from .base import CorridorGovernanceStrategy

class TreatyLifecycleFirstStrategy(CorridorGovernanceStrategy):
    def get_strategy_name(self) -> str:
        return "TreatyLifecycleFirstStrategy"

    def evaluate_visibility(self) -> str:
        return "lifecycle_driven"
