from .base import BaseRemediationLaneStrategy

class BalancedReviewAwareLaneStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "BalancedReviewAwareLaneStrategy"
