from .base import BaseExternalAuditStrategy
from typing import Dict, Any

class NotarizationFirstStrategy(BaseExternalAuditStrategy):
    def evaluate_external_input(self, input_data: Dict[str, Any]) -> str:
        if input_data.get("notarization_verified"):
            return "review"
        return "quarantine"

    def get_readiness_weights(self) -> Dict[str, float]:
        return {"notarization_coverage": 0.9, "packet_completeness": 0.1}
