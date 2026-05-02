from typing import Dict, Any
from .base import BaseEcosystemSyncStrategy

class QuarantineFirstSubscriptionStrategy(BaseEcosystemSyncStrategy):
    """Quarantine First strategy: anomalies trigger quick quarantine."""
    def get_strategy_name(self) -> str:
        return "QuarantineFirstSubscriptionStrategy"

    def execute_pass(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": self.get_strategy_name(), "status": "executed_mock"}
