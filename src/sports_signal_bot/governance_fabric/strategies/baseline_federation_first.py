from .base import BaseGovernanceFabricStrategy

class BaselineFederationFirstStrategy(BaseGovernanceFabricStrategy):
    def get_name(self) -> str:
        return "BaselineFederationFirstStrategy"

    def apply(self, context: dict) -> dict:
        # Prioritizes federated baseline currentness applicability
        return context
