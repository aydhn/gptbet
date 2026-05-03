from .base import CorridorGovernanceStrategy

class SovereigntyDominantCatalogStrategy(CorridorGovernanceStrategy):
    def get_strategy_name(self) -> str:
        return "SovereigntyDominantCatalogStrategy"

    def evaluate_visibility(self) -> str:
        return "sovereignty_restricted"
