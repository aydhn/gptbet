from typing import List, Dict
from .base import BaseTrustStrategy
from ..contracts import (
    ApprovalThresholdPolicyRecord,
    ApprovalSignerRecord,
    QuorumEvaluationRecord,
    VetoDecisionRecord,
    SignerGroupRecord
)

class EmergencyHardenedTrustStrategy(BaseTrustStrategy):
    """
    Emergency actions require the strictest signer mix, forced expiry, and post-review.
    """
    def evaluate(
        self,
        policy: ApprovalThresholdPolicyRecord,
        signers: List[ApprovalSignerRecord],
        vetoes: List[VetoDecisionRecord]
    ) -> QuorumEvaluationRecord:
        # Enforce that there are no review-only signers carrying the decision
        # by inflating the required trust threshold
        hardened_policy = policy.model_copy()
        hardened_policy.min_weighted_trust *= 1.5
        return super().evaluate(hardened_policy, signers, vetoes)
