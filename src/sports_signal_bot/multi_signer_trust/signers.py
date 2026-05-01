from typing import List, Dict, Optional
from .contracts import (
    ApprovalSignerRecord,
    SignerGroupRecord,
    SignerStatus,
    SignerTrustLevel
)

def compute_signer_weight(
    signer: ApprovalSignerRecord,
    group_configs: Dict[str, SignerGroupRecord],
    target_family: str
) -> float:
    """
    Computes the effective trust weight for a given signer, factoring in group
    memberships, status penalties, and target family capabilities.
    """
    if signer.status in [SignerStatus.REVOKED, SignerStatus.SUSPENDED]:
        return 0.0

    if signer.base_weight_override is not None:
        base_weight = signer.base_weight_override
    else:
        # Map trust level to a base weight
        level_map = {
            SignerTrustLevel.LOW: 0.1,
            SignerTrustLevel.MEDIUM: 0.5,
            SignerTrustLevel.HIGH: 1.0,
            SignerTrustLevel.CRITICAL_AUTHORITY: 2.0
        }
        base_weight = level_map.get(signer.trust_level, 0.0)

    # Status penalty
    if signer.status == SignerStatus.PROBATION:
        base_weight *= 0.5

    # Group modifiers
    max_group_weight = 0.0
    for group_name in signer.membership.group_names:
        if group_name in group_configs:
            group = group_configs[group_name]
            # Must be allowed for target family to contribute group weight
            if target_family in group.capabilities.allowed_target_families or "all" in group.capabilities.allowed_target_families:
                # Review-only penalty
                group_weight = group.trust_policy.base_weight
                if not group.capabilities.is_active_signing:
                    group_weight *= 0.25 # Review only penalty

                # Cap the weight
                group_weight = min(group_weight, group.trust_policy.max_weight_cap)
                if group_weight > max_group_weight:
                    max_group_weight = group_weight

    # Return base plus max group modifier (or just combination logic)
    final_weight = base_weight + max_group_weight
    return round(final_weight, 2)


def detect_unacceptable_trust_mix(signers: List[ApprovalSignerRecord]) -> bool:
    """
    Detects if a set of signers consists entirely of low-trust or review-only signers,
    which is an unacceptable mix for active critical paths.
    Returns True if unacceptable.
    """
    if not signers:
        return True

    for signer in signers:
        if signer.trust_level in [SignerTrustLevel.HIGH, SignerTrustLevel.CRITICAL_AUTHORITY] and signer.status == SignerStatus.ACTIVE:
            return False # Acceptable, has at least one high/critical active signer

    return True # Unacceptable, all are low/medium or not active
