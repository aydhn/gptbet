from typing import Dict, Any, List
from .base import BaseHandoffStrategy
from ..contracts import CouncilDecisionType, CouncilVoteLikeRecord

class ConservativeHandoffStrategy(BaseHandoffStrategy):
    def evaluate(self, context: Dict[str, Any], votes: List[CouncilVoteLikeRecord]) -> CouncilDecisionType:
        recs = [v.recommendation for v in votes]

        # Any blockers at all means hold
        if any(v.blockers for v in votes):
            return CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE

        if any(r == CouncilDecisionType.REJECT_HANDOFF for r in recs):
            return CouncilDecisionType.REJECT_HANDOFF

        if any(r == CouncilDecisionType.KILL_CANDIDATE_BEFORE_HANDOFF for r in recs):
             return CouncilDecisionType.KILL_CANDIDATE_BEFORE_HANDOFF

        if all(r == CouncilDecisionType.APPROVE_HANDOFF for r in recs) and not any(v.notes for v in votes):
            return CouncilDecisionType.UNANIMOUS_APPROVE

        return CouncilDecisionType.MIXED_HOLD
