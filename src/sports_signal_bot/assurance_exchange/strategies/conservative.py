from .base import BaseAssuranceExchangeStrategy
from typing import Dict, Any

class ConservativeAssuranceExchangeStrategy(BaseAssuranceExchangeStrategy):
    def get_name(self) -> str:
        return "ConservativeAssuranceExchangeStrategy"

    def get_quarantine_default(self) -> bool:
        return True

    def evaluate_acceptance(self, packet_id: str, context: Dict[str, Any]) -> str:
        # quarantine-first, translation tolerance low, replay mismatch hard block
        if context.get("translation_semantic_risk") in ["high", "medium"]:
            return "quarantined"
        if not context.get("replay_matched", False):
            return "blocked"
        return "accepted"
