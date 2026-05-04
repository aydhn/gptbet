import uuid
from typing import List
from .contracts import SovereignAuditDisputeRecord, DisputeCaseRecord

def open_sovereign_audit_dispute(family: str, source_ref: str, conflicting_refs: List[str]) -> SovereignAuditDisputeRecord:
    return SovereignAuditDisputeRecord(
        dispute_id=f"disp_{uuid.uuid4()}",
        dispute_family=family,
        source_projection_ref=source_ref,
        conflicting_projection_refs=conflicting_refs,
        affected_scope_ref="scope_global",
        opened_reason="projection_mismatch",
        dispute_status="dispute_opened"
    )

def run_dispute_mediation(dispute: SovereignAuditDisputeRecord, case: DisputeCaseRecord) -> str:
    if "sovereignty_deny" in case.sovereignty_constraints:
        return "preserve_local_deny"
    if case.replay_requirement == "mismatch":
        return "require_replay_rebuild"
    if not case.input_evidence_refs:
        return "downgrade_to_review_only"
    return "accept_bounded_projection_with_caveats"

def summarize_dispute_state(dispute: SovereignAuditDisputeRecord) -> dict:
    return {
        "id": dispute.dispute_id,
        "status": dispute.dispute_status,
        "conflict_count": len(dispute.conflicting_projection_refs)
    }
