from .base import BaseRemediationLaneStrategy

class TokenStrictStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "TokenStrictStrategy"
