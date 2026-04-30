from typing import Dict, Any, List
from .base import BaseHandoffStrategy
from ..contracts import CouncilDecisionType, CouncilVoteLikeRecord
from ..council import aggregate_council_lenses

class BalancedReadinessCouncilStrategy(BaseHandoffStrategy):
    def evaluate(self, context: Dict[str, Any], votes: List[CouncilVoteLikeRecord]) -> CouncilDecisionType:
        # Balanced strategy uses the standard aggregation
        return aggregate_council_lenses(votes)
