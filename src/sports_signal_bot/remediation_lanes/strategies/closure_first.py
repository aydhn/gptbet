from .base import BaseRemediationLaneStrategy

class ClosureFirstStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "ClosureFirstStrategy"
