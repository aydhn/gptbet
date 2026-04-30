from typing import List, Dict, Any, Optional
import datetime
from .contracts import ActivationDecisionRecord, ActivationDecisionType, PostActivationVerificationRecord, AdoptionRollbackRecord

def build_activation_evidence_packet(adoption_id: str, decision: ActivationDecisionType, council_ref: str, blockers: List[str], evidence_refs: List[str]) -> ActivationDecisionRecord:
    return ActivationDecisionRecord(
        activation_decision_id=f"dec_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoption_id=adoption_id,
        decision_type=decision,
        decision_status="finalized",
        council_ref=council_ref,
        blocker_refs=blockers,
        evidence_refs=evidence_refs,
        approval_status="approved" if decision == ActivationDecisionType.APPROVE_ACTIVATION else "held_or_rejected"
    )

def explain_activation_decision(decision: ActivationDecisionRecord) -> str:
    return f"Activation Decision: {decision.decision_type.value}. Blockers: {len(decision.blocker_refs)}. Evidence refs: {len(decision.evidence_refs)}."

def explain_verification_outcome(verification: PostActivationVerificationRecord) -> str:
    return f"Verification Outcome: {verification.overall_outcome.value}."

def explain_rollback_reason(rollback: AdoptionRollbackRecord) -> str:
    return f"Rollback Reason: {rollback.reason}. Target Snapshot: {rollback.target_snapshot_ref}."
