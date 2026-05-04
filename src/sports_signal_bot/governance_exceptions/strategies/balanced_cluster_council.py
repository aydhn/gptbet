from typing import Dict, Any
from .base import BaseGovernanceExceptionStrategy

class BalancedClusterCouncilStrategy(BaseGovernanceExceptionStrategy):
    @property
    def strategy_name(self) -> str:
        return "BalancedClusterCouncilStrategy"

    def evaluate(self, context: Dict[str, Any]) -> str:
        return "bounded_governance"
