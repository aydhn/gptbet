from typing import Dict, Any
from .base import BaseGovernanceExceptionStrategy

class ConservativeQuorumExchangeStrategy(BaseGovernanceExceptionStrategy):
    @property
    def strategy_name(self) -> str:
        return "ConservativeQuorumExchangeStrategy"

    def evaluate(self, context: Dict[str, Any]) -> str:
        # Default strategy. Very strict.
        return "review_only"
