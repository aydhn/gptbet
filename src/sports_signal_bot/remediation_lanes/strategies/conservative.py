from .base import BaseRemediationLaneStrategy

class ConservativeLaneExecutionStrategy(BaseRemediationLaneStrategy):
    def get_strategy_name(self) -> str:
        return "ConservativeLaneExecutionStrategy"
