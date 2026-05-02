from .base import BaseAssuranceExchangeStrategy
from typing import Dict, Any

class ReplayStrictFederationStrategy(BaseAssuranceExchangeStrategy):
    def get_name(self) -> str:
        return "ReplayStrictFederationStrategy"

    def get_quarantine_default(self) -> bool:
        return True

    def evaluate_acceptance(self, packet_id: str, context: Dict[str, Any]) -> str:
        if context.get("replay_matched", False):
            return "accepted"
        return "blocked"
