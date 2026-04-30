from typing import Dict, Any, List
from ..contracts import StableAdoptionRecord, ActivationDecisionType, AdoptionBlockerRecord

class BaseAdoptionStrategy:
    def evaluate_adoption(self, adoption: StableAdoptionRecord, blockers: List[AdoptionBlockerRecord], readiness: Any) -> ActivationDecisionType:
        raise NotImplementedError("Must be implemented by subclasses")
