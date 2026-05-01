from typing import List, Dict
from .base import BaseTrustStrategy
from ..contracts import (
    ApprovalThresholdPolicyRecord,
    ApprovalSignerRecord,
    QuorumEvaluationRecord,
    VetoDecisionRecord,
    SignerGroupRecord
)

class DevCompatibleButScopedStrategy(BaseTrustStrategy):
    """
    Supports dev/test bundle flow but never leaks into active governance paths.
    """
    def evaluate(
        self,
        policy: ApprovalThresholdPolicyRecord,
        signers: List[ApprovalSignerRecord],
        vetoes: List[VetoDecisionRecord]
    ) -> QuorumEvaluationRecord:
        # Dev strategy allows easier quorum for scoped dev tasks
        dev_policy = policy.model_copy()
        if "dev_sandbox" in dev_policy.target_scope.get("environment", []):
            dev_policy.min_signer_count = 1
            dev_policy.min_weighted_trust = 0.5
        return super().evaluate(dev_policy, signers, vetoes)
