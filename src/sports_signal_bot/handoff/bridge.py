import uuid
from typing import Dict, Any, List
from .contracts import ActivationBridgePackageRecord, CouncilDecisionType

def build_activation_bridge(
    handoff_id: str,
    candidate_refs: List[str],
    decision_ref: str,
    context: Dict[str, Any]
) -> ActivationBridgePackageRecord:

    constraints = []
    reasons = []

    if context.get("scope", "broad") == "broad":
        constraints.append("Broad scope requires staggered percentage rollout.")

    if not context.get("monitoring_expectations_defined", False):
        constraints.append("Must define monitoring dashboard before activation.")

    if context.get("decision_type") != CouncilDecisionType.APPROVE_HANDOFF and \
       context.get("decision_type") != CouncilDecisionType.READY_FOR_ACTIVATION_BRIDGE_ONLY:
        reasons.append(f"Handoff not fully approved. Status: {context.get('decision_type', 'unknown')}")

    return ActivationBridgePackageRecord(
        bridge_package_id=str(uuid.uuid4()),
        handoff_id=handoff_id,
        candidate_package_refs=candidate_refs,
        council_decision_ref=decision_ref,
        required_final_approvals=["Release Manager"] if not context.get("approvals_complete", False) else [],
        required_post_handoff_checks=["Verify Monitoring Hooks"],
        adoption_scope_hints=[f"Scope is {context.get('scope', 'unknown')}"],
        rollback_safety_notes=["Use standard shadow fallback"] if context.get("rollback_ready", False) else ["WARNING: Rollback undefined"],
        activation_constraints=constraints,
        do_not_activate_reasons=reasons
    )

def validate_bridge_prerequisites(bridge: ActivationBridgePackageRecord) -> bool:
    return len(bridge.do_not_activate_reasons) == 0

def attach_activation_constraints(bridge: ActivationBridgePackageRecord, new_constraints: List[str]) -> ActivationBridgePackageRecord:
    bridge.activation_constraints.extend(new_constraints)
    return bridge

def summarize_bridge_readiness(bridge: ActivationBridgePackageRecord) -> str:
    if bridge.do_not_activate_reasons:
        return f"Not ready for activation. {len(bridge.do_not_activate_reasons)} blocking reasons."
    elif bridge.activation_constraints:
        return f"Ready with {len(bridge.activation_constraints)} constraints."
    return "Ready for unrestricted activation."
