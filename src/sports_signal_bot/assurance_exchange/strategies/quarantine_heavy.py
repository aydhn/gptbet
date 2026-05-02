from .base import BaseAssuranceExchangeStrategy
from typing import Dict, Any

class QuarantineHeavyInteropStrategy(BaseAssuranceExchangeStrategy):
    def get_name(self) -> str:
        return "QuarantineHeavyInteropStrategy"

    def get_quarantine_default(self) -> bool:
        return True

    def evaluate_acceptance(self, packet_id: str, context: Dict[str, Any]) -> str:
        if not context.get("fully_known", False):
            return "quarantined"
        return "accepted"
