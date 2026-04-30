from typing import Dict, Any, List
from .base import BaseAdoptionStrategy
from ..contracts import StableAdoptionRecord, ActivationDecisionType, AdoptionBlockerRecord

class NarrowScopeIncrementalAdoptionStrategy(BaseAdoptionStrategy):
    def evaluate_adoption(self, adoption: StableAdoptionRecord, blockers: List[AdoptionBlockerRecord], readiness: Any) -> ActivationDecisionType:
        if adoption.adoption_scope == "global":
            return ActivationDecisionType.REQUIRE_NARROWER_SCOPE
        if blockers:
            return ActivationDecisionType.HOLD_ACTIVATION
        return ActivationDecisionType.APPROVE_ACTIVATION
