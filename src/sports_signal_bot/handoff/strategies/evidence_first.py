from typing import Dict, Any, List
from .base import BaseHandoffStrategy
from ..contracts import CouncilDecisionType, CouncilVoteLikeRecord

class EvidenceFirstHandoffStrategy(BaseHandoffStrategy):
    def evaluate(self, context: Dict[str, Any], votes: List[CouncilVoteLikeRecord]) -> CouncilDecisionType:
        evidence_vote = next((v for v in votes if v.lens_name == "evidence_lens"), None)
        sim_vote = next((v for v in votes if v.lens_name == "simulation_lens"), None)

        if evidence_vote and evidence_vote.recommendation == CouncilDecisionType.REJECT_HANDOFF:
             return CouncilDecisionType.REJECT_HANDOFF
        if sim_vote and sim_vote.recommendation == CouncilDecisionType.REJECT_HANDOFF:
             return CouncilDecisionType.REJECT_HANDOFF

        if evidence_vote and evidence_vote.recommendation == CouncilDecisionType.APPROVE_HANDOFF and \
           sim_vote and sim_vote.recommendation == CouncilDecisionType.APPROVE_HANDOFF:

            # Check for critical governance blockers, but be lenient on notes
            gov_vote = next((v for v in votes if v.lens_name == "governance_lens"), None)
            if gov_vote and gov_vote.blockers:
                return CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE
            return CouncilDecisionType.APPROVE_WITH_CAVEATS

        return CouncilDecisionType.MIXED_HOLD
