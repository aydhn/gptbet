from typing import Dict, Any, List
from .base import BaseHandoffStrategy
from ..contracts import CouncilDecisionType, CouncilVoteLikeRecord

class GovernanceHeavyHandoffStrategy(BaseHandoffStrategy):
    def evaluate(self, context: Dict[str, Any], votes: List[CouncilVoteLikeRecord]) -> CouncilDecisionType:
        gov_vote = next((v for v in votes if v.lens_name == "governance_lens"), None)

        if not gov_vote or gov_vote.recommendation != CouncilDecisionType.APPROVE_HANDOFF:
            return CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE

        # Delegate to standard aggregation if governance is clean
        recs = [v.recommendation for v in votes]
        if any(r == CouncilDecisionType.REJECT_HANDOFF for r in recs):
            return CouncilDecisionType.REJECT_HANDOFF

        if all(r == CouncilDecisionType.APPROVE_HANDOFF for r in recs):
            return CouncilDecisionType.UNANIMOUS_APPROVE

        return CouncilDecisionType.APPROVE_WITH_CAVEATS
