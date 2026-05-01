from .base import BaseExternalAuditStrategy
from typing import Dict, Any

class ReputationAwareChallengeStrategy(BaseExternalAuditStrategy):
    def evaluate_external_input(self, input_data: Dict[str, Any]) -> str:
        if input_data.get("reputation", 0) > 80:
            return "review"
        return "quarantine"

    def get_readiness_weights(self) -> Dict[str, float]:
        return {"witness_reputation_stability": 0.8, "responder_diversity": 0.2}
