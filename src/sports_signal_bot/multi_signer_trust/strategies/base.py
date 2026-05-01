from typing import List, Dict
from ..contracts import (
    ApprovalThresholdPolicyRecord,
    ApprovalSignerRecord,
    QuorumEvaluationRecord,
    VetoDecisionRecord,
    SignerGroupRecord
)
from ..thresholds import summarize_threshold_result

class BaseTrustStrategy:
    def __init__(self, group_configs: Dict[str, SignerGroupRecord]):
        self.group_configs = group_configs

    def evaluate(
        self,
        policy: ApprovalThresholdPolicyRecord,
        signers: List[ApprovalSignerRecord],
        vetoes: List[VetoDecisionRecord]
    ) -> QuorumEvaluationRecord:
        return summarize_threshold_result(signers, policy, self.group_configs, vetoes)
