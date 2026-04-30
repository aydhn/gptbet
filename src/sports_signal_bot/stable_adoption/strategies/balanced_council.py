from typing import Dict, Any, List
from .base import BaseAdoptionStrategy
from ..contracts import StableAdoptionRecord, ActivationDecisionType, AdoptionBlockerRecord

class BalancedActivationCouncilStrategy(BaseAdoptionStrategy):
    def evaluate_adoption(self, adoption: StableAdoptionRecord, blockers: List[AdoptionBlockerRecord], readiness: Any) -> ActivationDecisionType:
        critical_blockers = [b for b in blockers if b.severity == "critical"]
        if critical_blockers:
            return ActivationDecisionType.REJECT_ACTIVATION
        if not readiness or not getattr(readiness, 'is_ready', False):
            return ActivationDecisionType.HOLD_ACTIVATION
        return ActivationDecisionType.APPROVE_ACTIVATION
