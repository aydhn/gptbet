from typing import Dict, Any
from .base import BaseGovernanceExceptionStrategy

class BaselineCouncilFirstStrategy(BaseGovernanceExceptionStrategy):
    @property
    def strategy_name(self) -> str:
        return "BaselineCouncilFirstStrategy"

    def evaluate(self, context: Dict[str, Any]) -> str:
        return "baseline_adjudicated"
