from typing import Dict, Any, List
from .base import BaseHandoffStrategy
from ..contracts import CouncilDecisionType, CouncilVoteLikeRecord

class NarrowScopeFastBridgeStrategy(BaseHandoffStrategy):
    def evaluate(self, context: Dict[str, Any], votes: List[CouncilVoteLikeRecord]) -> CouncilDecisionType:
        if context.get("scope", "broad") != "narrow":
            return CouncilDecisionType.MIXED_HOLD # Fail back to standard path if not narrow

        # Very tolerant for narrow scope
        recs = [v.recommendation for v in votes]
        if any(r == CouncilDecisionType.KILL_CANDIDATE_BEFORE_HANDOFF for r in recs):
             return CouncilDecisionType.KILL_CANDIDATE_BEFORE_HANDOFF

        return CouncilDecisionType.READY_FOR_ACTIVATION_BRIDGE_ONLY
