from typing import Dict, Any, List
from .base import BaseAdoptionStrategy
from ..contracts import StableAdoptionRecord, ActivationDecisionType, AdoptionBlockerRecord

class EvidenceFirstActivationStrategy(BaseAdoptionStrategy):
    def evaluate_adoption(self, adoption: StableAdoptionRecord, blockers: List[AdoptionBlockerRecord], readiness: Any) -> ActivationDecisionType:
        if blockers:
            return ActivationDecisionType.REQUIRE_MORE_EVIDENCE
        return ActivationDecisionType.APPROVE_ACTIVATION
