from .base import BaseExternalAuditStrategy
from typing import Dict, Any

class QuarantineHeavyExternalInputStrategy(BaseExternalAuditStrategy):
    def evaluate_external_input(self, input_data: Dict[str, Any]) -> str:
        if input_data.get("reputation", 0) > 90 and input_data.get("verified_local", False):
            return "verified_supporting"
        return "quarantine"

    def get_readiness_weights(self) -> Dict[str, float]:
        return {"quarantine_discipline": 1.0}
