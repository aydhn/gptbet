from typing import Optional
from typing import List, Dict, Tuple
from datetime import datetime
from .contracts import (
    ApprovalThresholdPolicyRecord,
    ApprovalSignerRecord,
    QuorumEvaluationRecord,
    WeightedTrustRecord,
    VetoDecisionRecord,
    SignerGroupRecord,
    MandatoryPresenceRuleRecord,
    VetoRuleRecord
)
from .signers import compute_signer_weight


def evaluate_signer_count_threshold(
    signers: List[ApprovalSignerRecord],
    min_count: int
) -> bool:
    # Only count valid signers
    valid_count = sum(1 for s in signers if s.status.value in ["active", "probation"])
    return valid_count >= min_count


def compute_weighted_trust_total(
    signers: List[ApprovalSignerRecord],
    group_configs: Dict[str, SignerGroupRecord],
    target_family: str
) -> Tuple[float, List[WeightedTrustRecord]]:
    records = []
    total = 0.0
    for s in signers:
        weight = compute_signer_weight(s, group_configs, target_family)
        total += weight
        records.append(WeightedTrustRecord(
            signer_id=s.signer_id,
            computed_weight=weight,
            modifiers_applied=["base", "group"] if weight > 0 else [],
            is_capped=False
        ))
    return round(total, 2), records


def evaluate_weighted_trust_threshold(
    total_trust: float,
    min_trust: float
) -> bool:
    return total_trust >= min_trust


def evaluate_mandatory_presence(
    signers: List[ApprovalSignerRecord],
    mandatory_rules: List[MandatoryPresenceRuleRecord]
) -> bool:
    if not mandatory_rules:
        return True

    # Build group counts
    group_counts = {}
    for s in signers:
        if s.status.value in ["active", "probation"]:
            for group in s.membership.group_names:
                group_counts[group] = group_counts.get(group, 0) + 1

    for rule in mandatory_rules:
        if group_counts.get(rule.required_group, 0) < rule.min_count:
            return False

    return True

# Alias for backward compatibility based on plan wording
evaluate_mandatory_signers = evaluate_mandatory_presence


def evaluate_cross_group_diversity(
    signers: List[ApprovalSignerRecord],
    min_groups: int = 1
) -> bool:
    unique_groups = set()
    for s in signers:
         if s.status.value in ["active", "probation"]:
             for g in s.membership.group_names:
                 unique_groups.add(g)
    return len(unique_groups) >= min_groups


def evaluate_veto_rules(
    vetoes: List[VetoDecisionRecord],
    policy_veto_rules: Optional[VetoRuleRecord]
) -> bool:
    # Returns True if veto blocks the approval
    if not policy_veto_rules or not vetoes:
        return False

    for veto in vetoes:
        if veto.group_name in policy_veto_rules.veto_enabled_groups:
            return True

    return False


def explain_veto_block(vetoes: List[VetoDecisionRecord]) -> str:
    if not vetoes:
        return "No vetoes present."
    reasons = [f"{v.signer_id} ({v.group_name}): {v.reason}" for v in vetoes]
    return "Veto Blocked by: " + "; ".join(reasons)


def differentiate_threshold_fail_vs_veto_block(
    quorum_eval: QuorumEvaluationRecord
) -> str:
    if quorum_eval.vetoes_present:
        return "VETO_BLOCK"
    if not quorum_eval.signer_count_satisfied:
        return "SIGNER_COUNT_FAIL"
    if not quorum_eval.weighted_trust_satisfied:
        return "WEIGHTED_TRUST_FAIL"
    if not quorum_eval.mandatory_presence_satisfied:
        return "MANDATORY_PRESENCE_FAIL"
    return "SATISFIED"


def explain_weighted_trust_breakdown(records: List[WeightedTrustRecord]) -> str:
    return ", ".join([f"{r.signer_id}={r.computed_weight}" for r in records])


def summarize_threshold_result(
    signers: List[ApprovalSignerRecord],
    policy: ApprovalThresholdPolicyRecord,
    group_configs: Dict[str, SignerGroupRecord],
    vetoes: List[VetoDecisionRecord]
) -> QuorumEvaluationRecord:
    total_trust, records = compute_weighted_trust_total(signers, group_configs, policy.policy_family)

    count_ok = evaluate_signer_count_threshold(signers, policy.min_signer_count)
    trust_ok = evaluate_weighted_trust_threshold(total_trust, policy.min_weighted_trust)
    mandatory_ok = evaluate_mandatory_presence(signers, policy.mandatory_signer_groups)
    veto_present = evaluate_veto_rules(vetoes, policy.veto_rules)

    return QuorumEvaluationRecord(
        evaluation_id=f"eval_{datetime.utcnow().timestamp()}",
        policy_ref=policy.threshold_policy_id,
        signer_count_satisfied=count_ok,
        weighted_trust_satisfied=trust_ok,
        mandatory_presence_satisfied=mandatory_ok,
        vetoes_present=veto_present,
        total_signers=len(signers),
        total_weighted_trust=total_trust,
        veto_records=vetoes
    )
