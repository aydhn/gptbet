from typing import Dict, Any, List
from .base import BaseAdoptionStrategy
from ..contracts import StableAdoptionRecord, ActivationDecisionType, AdoptionBlockerRecord

class ConservativeStableAdoptionStrategy(BaseAdoptionStrategy):
    def evaluate_adoption(self, adoption: StableAdoptionRecord, blockers: List[AdoptionBlockerRecord], readiness: Any) -> ActivationDecisionType:
        if blockers:
            return ActivationDecisionType.REJECT_ACTIVATION
        if not readiness or not getattr(readiness, 'is_ready', False):
            return ActivationDecisionType.HOLD_ACTIVATION
        if adoption.adoption_scope != "narrow":
            return ActivationDecisionType.REQUIRE_NARROWER_SCOPE
        return ActivationDecisionType.APPROVE_ACTIVATION
