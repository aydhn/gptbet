from .base import BaseRemediationLaneStrategy

class FederatedCatalogAwareLaneStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "FederatedCatalogAwareLaneStrategy"
