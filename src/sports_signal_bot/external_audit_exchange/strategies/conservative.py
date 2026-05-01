from .base import BaseExternalAuditStrategy
from typing import Dict, Any

class ConservativeExternalAuditStrategy(BaseExternalAuditStrategy):
    def evaluate_external_input(self, input_data: Dict[str, Any]) -> str:
        return "quarantine" # Default to quarantine

    def get_readiness_weights(self) -> Dict[str, float]:
        return {"quarantine_discipline": 0.8, "packet_completeness": 0.2}
