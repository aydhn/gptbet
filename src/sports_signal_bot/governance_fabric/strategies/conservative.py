from .base import BaseGovernanceFabricStrategy

class ConservativeCouncilFabricStrategy(BaseGovernanceFabricStrategy):
    def get_name(self) -> str:
        return "ConservativeCouncilFabricStrategy"

    def apply(self, context: dict) -> dict:
        # Aggressive suppression, high evidence threshold, early escalation
        return context
