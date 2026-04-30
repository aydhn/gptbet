from typing import Dict, Any, List
from .base import BaseAdoptionStrategy
from ..contracts import StableAdoptionRecord, ActivationDecisionType, AdoptionBlockerRecord

class RollbackFirstSafetyStrategy(BaseAdoptionStrategy):
    def evaluate_adoption(self, adoption: StableAdoptionRecord, blockers: List[AdoptionBlockerRecord], readiness: Any) -> ActivationDecisionType:
        if not readiness or not getattr(readiness, 'is_ready', False):
            return ActivationDecisionType.REJECT_ACTIVATION
        if blockers:
            return ActivationDecisionType.HOLD_ACTIVATION
        return ActivationDecisionType.APPROVE_ACTIVATION
