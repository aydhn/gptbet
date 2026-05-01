from typing import List, Dict
from .base import BaseTrustStrategy
from ..contracts import (
    ApprovalThresholdPolicyRecord,
    ApprovalSignerRecord,
    QuorumEvaluationRecord,
    VetoDecisionRecord,
    SignerGroupRecord
)

class ReviewQuarantineHeavyStrategy(BaseTrustStrategy):
    """
    Incomplete trust items quickly fall to quarantine; active path is extremely strict.
    """
    def evaluate(
        self,
        policy: ApprovalThresholdPolicyRecord,
        signers: List[ApprovalSignerRecord],
        vetoes: List[VetoDecisionRecord]
    ) -> QuorumEvaluationRecord:
        # Require more signers or higher trust than the base policy
        strict_policy = policy.model_copy()
        strict_policy.min_signer_count = max(policy.min_signer_count, 2)
        strict_policy.min_weighted_trust = max(policy.min_weighted_trust, 2.0)
        return super().evaluate(strict_policy, signers, vetoes)
