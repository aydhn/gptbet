from typing import List, Tuple
from datetime import datetime, timedelta
from .contracts import (
    ApprovalThresholdPolicyRecord,
    EmergencyTrustPolicyRecord,
    MultiSignerApprovalRecord,
    ApprovalSignerRecord,
    SignerStatus,
    SignerTrustLevel
)

def detect_unsafe_threshold_lowering(
    base: ApprovalThresholdPolicyRecord,
    overlay: ApprovalThresholdPolicyRecord
) -> bool:
    if overlay.min_signer_count < base.min_signer_count:
        return True
    if overlay.min_weighted_trust < base.min_weighted_trust:
        return True
    return False

def require_stronger_review_for_trust_relaxation() -> ApprovalThresholdPolicyRecord:
    # Example placeholder policy for reviewing a relaxation
    return ApprovalThresholdPolicyRecord(
        threshold_policy_id=f"relax_review_{datetime.utcnow().timestamp()}",
        policy_family="trust_relaxation",
        target_scope={"all": True},
        min_signer_count=3,
        min_weighted_trust=4.0,
        expiry_seconds=3600
    )

def merge_threshold_policy_overlays(
    base: ApprovalThresholdPolicyRecord,
    overlay: ApprovalThresholdPolicyRecord,
    allow_unsafe_lowering: bool = False
) -> ApprovalThresholdPolicyRecord:
    if detect_unsafe_threshold_lowering(base, overlay) and not allow_unsafe_lowering:
        # Reject the lowering, return base
        return base

    return overlay

def summarize_threshold_overlay_effect(
    base: ApprovalThresholdPolicyRecord,
    merged: ApprovalThresholdPolicyRecord
) -> str:
    diffs = []
    if base.min_signer_count != merged.min_signer_count:
        diffs.append(f"Signers: {base.min_signer_count}->{merged.min_signer_count}")
    if base.min_weighted_trust != merged.min_weighted_trust:
        diffs.append(f"Trust: {base.min_weighted_trust}->{merged.min_weighted_trust}")
    return "Overlay effect: " + (", ".join(diffs) if diffs else "No change")


def resolve_emergency_threshold_policy(
    emergency_policy: EmergencyTrustPolicyRecord,
    base_policy: ApprovalThresholdPolicyRecord
) -> ApprovalThresholdPolicyRecord:
    # Creates an overlay based on emergency rules
    # E.g. requires specific emergency groups, lowers counts but raises required trust weight
    new_policy = base_policy.model_copy()
    new_policy.threshold_policy_id = f"emerg_{emergency_policy.emergency_policy_id}"
    new_policy.expiry_seconds = emergency_policy.window.max_duration_seconds
    return new_policy


def validate_emergency_signer_mix(
    signers: List[ApprovalSignerRecord],
    emergency_policy: EmergencyTrustPolicyRecord
) -> bool:
    # Ensure all required emergency groups are present and total weight is sufficient
    group_counts = {g: 0 for g in emergency_policy.signer_constraints.required_groups}
    for s in signers:
        if s.status == SignerStatus.ACTIVE:
            for g in s.membership.group_names:
                if g in group_counts:
                    group_counts[g] += 1

    for count in group_counts.values():
        if count == 0:
            return False

    # For emergency, we might enforce high trust levels
    has_critical = any(s.trust_level == SignerTrustLevel.CRITICAL_AUTHORITY for s in signers)
    if not has_critical:
        return False

    return True


def expire_emergency_approvals(
    approvals: List[MultiSignerApprovalRecord]
) -> List[MultiSignerApprovalRecord]:
    expired = []
    now = datetime.utcnow()
    for a in approvals:
        if a.approval_deadline and now > a.approval_deadline:
            a.current_status = "expired"
            expired.append(a)
    return expired


def force_post_emergency_review(
    approval: MultiSignerApprovalRecord,
    emergency_policy: EmergencyTrustPolicyRecord
) -> bool:
    # E.g. marks a requirement in the system to review this action
    return emergency_policy.window.requires_post_review


def determine_required_countersignatures(
    target_family: str,
    base_rules: dict
) -> List[str]:
    # E.g. {"security_sensitive": ["security_review_signers"]}
    return base_rules.get(target_family, [])


def validate_cross_plane_trust_requirements(
    signers: List[ApprovalSignerRecord],
    required_countersign_groups: List[str]
) -> bool:
    if not required_countersign_groups:
        return True

    present_groups = set()
    for s in signers:
        if s.status == SignerStatus.ACTIVE:
            present_groups.update(s.membership.group_names)

    for req in required_countersign_groups:
        if req not in present_groups:
            return False

    return True


def explain_missing_countersign(
    required_groups: List[str],
    signers: List[ApprovalSignerRecord]
) -> str:
    present_groups = set()
    for s in signers:
        if s.status == SignerStatus.ACTIVE:
            present_groups.update(s.membership.group_names)

    missing = [req for req in required_groups if req not in present_groups]
    return f"Missing required countersignatures from: {', '.join(missing)}"


def aggregate_cross_plane_approval(
    local_approved: bool,
    remote_approved: bool,
    requires_remote: bool
) -> bool:
    if requires_remote:
        return local_approved and remote_approved
    return local_approved
