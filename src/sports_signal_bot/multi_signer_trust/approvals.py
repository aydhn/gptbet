from datetime import datetime
from typing import List, Optional, Dict
from .contracts import (
    MultiSignerApprovalRecord,
    ApprovalStatus,
    SignerQuorumSetRecord,
    ApprovalThresholdPolicyRecord,
    ApprovalSignerRecord,
    VetoDecisionRecord,
    SignerGroupRecord,
    QuorumEvaluationRecord
)
from .thresholds import summarize_threshold_result

def build_multi_signer_approval(
    target_family: str,
    target_ref: str,
    policy_ref: str,
    required_quorum: SignerQuorumSetRecord,
    deadline: Optional[datetime] = None
) -> MultiSignerApprovalRecord:
    return MultiSignerApprovalRecord(
        multi_approval_id=f"appr_{datetime.utcnow().timestamp()}",
        target_family=target_family,
        target_ref=target_ref,
        approval_policy_ref=policy_ref,
        required_quorum=required_quorum,
        collected_signatures=[],
        current_status=ApprovalStatus.CREATED,
        approval_deadline=deadline
    )

def add_signature_to_approval(
    approval: MultiSignerApprovalRecord,
    signer_id: str
) -> MultiSignerApprovalRecord:
    if signer_id not in approval.collected_signatures:
        approval.collected_signatures.append(signer_id)
        if approval.current_status == ApprovalStatus.CREATED:
            approval.current_status = ApprovalStatus.COLLECTING
    return approval

def evaluate_approval_progress(
    approval: MultiSignerApprovalRecord,
    signers: List[ApprovalSignerRecord],
    group_configs: Dict[str, SignerGroupRecord],
    vetoes: List[VetoDecisionRecord]
) -> QuorumEvaluationRecord:
    # Use first policy from quorum set for basic evaluation
    policy = approval.required_quorum.required_policies[0]

    # Filter signers to those who have signed
    active_signers = [s for s in signers if s.signer_id in approval.collected_signatures]

    eval_result = summarize_threshold_result(
        signers=active_signers,
        policy=policy,
        group_configs=group_configs,
        vetoes=vetoes
    )

    approval.weighted_trust_total = eval_result.total_weighted_trust

    if eval_result.vetoes_present:
        approval.current_status = ApprovalStatus.THRESHOLD_FAILED
    elif eval_result.signer_count_satisfied and eval_result.weighted_trust_satisfied and eval_result.mandatory_presence_satisfied:
        approval.current_status = ApprovalStatus.THRESHOLD_SATISFIED
    else:
        approval.current_status = ApprovalStatus.COLLECTING

    return eval_result

def finalize_threshold_decision(
    approval: MultiSignerApprovalRecord,
    attestation_pending: bool = False
) -> None:
    if approval.current_status == ApprovalStatus.THRESHOLD_SATISFIED:
        if attestation_pending:
            approval.current_status = ApprovalStatus.PENDING_ATTESTATION
        else:
            approval.current_status = ApprovalStatus.FULLY_VERIFIED

def archive_expired_approval(
    approval: MultiSignerApprovalRecord
) -> None:
    if approval.approval_deadline and datetime.utcnow() > approval.approval_deadline:
        approval.current_status = ApprovalStatus.EXPIRED
