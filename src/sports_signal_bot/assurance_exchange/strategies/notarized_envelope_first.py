from .base import BaseAssuranceExchangeStrategy
from typing import Dict, Any

class NotarizedEnvelopeFirstStrategy(BaseAssuranceExchangeStrategy):
    def get_name(self) -> str:
        return "NotarizedEnvelopeFirstStrategy"

    def get_quarantine_default(self) -> bool:
        return False

    def evaluate_acceptance(self, packet_id: str, context: Dict[str, Any]) -> str:
        if context.get("is_notarized", False):
            if context.get("replay_matched", False):
                return "accepted"
            else:
                return "review_required"
        return "quarantined"
