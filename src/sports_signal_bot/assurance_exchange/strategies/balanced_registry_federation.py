from .base import BaseAssuranceExchangeStrategy
from typing import Dict, Any

class BalancedRegistryFederationStrategy(BaseAssuranceExchangeStrategy):
    def get_name(self) -> str:
        return "BalancedRegistryFederationStrategy"

    def get_quarantine_default(self) -> bool:
        return False

    def evaluate_acceptance(self, packet_id: str, context: Dict[str, Any]) -> str:
        # balanced
        if context.get("translation_semantic_risk") == "high":
            return "quarantined"
        if not context.get("replay_matched", False):
            return "review_required"
        return "accepted"
