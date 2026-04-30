import uuid
from typing import Dict, Any, List
from .contracts import CouncilDecisionRecord, CouncilDecisionType

def create_council_decision(
    handoff_id: str,
    aggregated_decision: CouncilDecisionType,
    context: Dict[str, Any],
    blockers: List[str] = None,
    evidence_refs: List[str] = None
) -> CouncilDecisionRecord:

    # Map internal aggregated outcomes to final decision types
    if aggregated_decision == CouncilDecisionType.UNANIMOUS_APPROVE:
        final_decision = CouncilDecisionType.APPROVE_HANDOFF
        status = "approved"
    elif aggregated_decision == CouncilDecisionType.APPROVE_WITH_CAVEATS:
        final_decision = CouncilDecisionType.APPROVE_HANDOFF
        status = "approved_with_caveats"
    elif aggregated_decision == CouncilDecisionType.MIXED_HOLD:
        # Determine specific hold reason
        if not context.get("approvals_complete", False):
            final_decision = CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE
        elif context.get("stale_simulation", False):
            final_decision = CouncilDecisionType.REQUIRE_ADDITIONAL_SIMULATION
        else:
            final_decision = CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE
        status = "held"
    elif aggregated_decision == CouncilDecisionType.REJECT_HANDOFF:
        final_decision = CouncilDecisionType.REJECT_HANDOFF
        status = "rejected"
    elif aggregated_decision == CouncilDecisionType.KILL_CANDIDATE_BEFORE_HANDOFF:
        final_decision = CouncilDecisionType.KILL_CANDIDATE_BEFORE_HANDOFF
        status = "killed"
    else:
        final_decision = aggregated_decision
        status = "pending"

    # Only set bridge ready if narrow scope override applies (simplified)
    if context.get("bridge_ready_only", False) and status == "approved":
        final_decision = CouncilDecisionType.READY_FOR_ACTIVATION_BRIDGE_ONLY
        status = "bridge_ready"

    return CouncilDecisionRecord(
        decision_id=str(uuid.uuid4()),
        handoff_id=handoff_id,
        decision_type=final_decision,
        decision_status=status,
        blocker_refs=blockers or [],
        evidence_refs=evidence_refs or [],
        required_followups=[],
        approval_status="complete" if context.get("approvals_complete", False) else "pending"
    )
