from .base import CorridorGovernanceStrategy

class ConservativeCorridorCatalogStrategy(CorridorGovernanceStrategy):
    def get_strategy_name(self) -> str:
        return "ConservativeCorridorCatalogStrategy"

    def evaluate_visibility(self) -> str:
        return "strict"
