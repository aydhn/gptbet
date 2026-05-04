import uuid
from typing import List

from .contracts import (
    SovereignProjectionAuditExchangeRecord, ProjectionAuditPacketRecord,
    ProjectionAuditEvidenceRecord, ProjectionAuditReplayRecord,
    ProjectionAuditDecisionRecord
)

def build_projection_audit_packet(
    source_refs: List[str], evidence_refs: List[str], caveats: List[str]
) -> ProjectionAuditPacketRecord:
    status = "audit_prepared"
    warnings = []

    if not evidence_refs:
        status = "audit_blocked"
        warnings.append("Audit packet without evidence accepted as verified block")

    return ProjectionAuditPacketRecord(
        audit_packet_id=f"packet_{uuid.uuid4().hex[:8]}",
        source_projection_refs=source_refs,
        preserved_caveat_refs=caveats,
        currentness_refs=["curr_1"],
        projection_method_summary="bounded_projection",
        evidence_refs=evidence_refs,
        validity_window="24h",
        audit_status=status,
        warnings=warnings
    )

def verify_projection_audit_exchange(
    packet: ProjectionAuditPacketRecord, target_scope: str, has_sovereignty_deny: bool
) -> SovereignProjectionAuditExchangeRecord:

    if has_sovereignty_deny:
        packet.audit_status = "audit_blocked"
        packet.warnings.append("Sovereignty deny masked by council or audit result block")
    elif packet.audit_status == "audit_prepared":
        if packet.preserved_caveat_refs:
            packet.audit_status = "audit_verified_with_caveats"
        else:
            packet.audit_status = "audit_verified"

    return SovereignProjectionAuditExchangeRecord(
        audit_exchange_id=f"exchange_{uuid.uuid4().hex[:8]}",
        source_scope_ref="source_1",
        target_scope_ref=target_scope,
        audit_packet_refs=[packet.audit_packet_id],
        exchange_scope="bounded_exchange",
        replay_support_refs=[],
        verification_refs=["ver_1"],
        decision_refs=[],
        health_status="healthy" if not has_sovereignty_deny else "blocked",
        warnings=[] if not has_sovereignty_deny else ["Sovereignty Deny applied"]
    )

def replay_projection_audit_packet(packet: ProjectionAuditPacketRecord, mismatch: bool) -> ProjectionAuditReplayRecord:
    outcome = "replay_matched"
    if mismatch:
        outcome = "replay_currentness_drifted"
        packet.audit_status = "audit_replay_required"
        packet.warnings.append("Audit replay mismatch")

    return ProjectionAuditReplayRecord(
        replay_id=f"replay_{uuid.uuid4().hex[:8]}",
        packet_ref=packet.audit_packet_id,
        replay_outcome=outcome,
        drift_details="Mismatch detected" if mismatch else "None"
    )

def downgrade_projection_on_audit_mismatch(exchange: SovereignProjectionAuditExchangeRecord, replay: ProjectionAuditReplayRecord) -> ProjectionAuditDecisionRecord:
    status = "approved"
    caps = []

    if "drift" in replay.replay_outcome or "mismatch" in replay.drift_details.lower():
        status = "capped"
        caps.append("Downgraded due to replay mismatch")
        exchange.health_status = "degraded"
        exchange.warnings.append("Projection capped by controller due to audit mismatch")

    decision = ProjectionAuditDecisionRecord(
        decision_id=f"dec_{uuid.uuid4().hex[:8]}",
        exchange_ref=exchange.audit_exchange_id,
        final_status=status,
        applied_caps=caps
    )
    exchange.decision_refs.append(decision.decision_id)
    return decision

def summarize_projection_audit_exchange(exchange: SovereignProjectionAuditExchangeRecord) -> str:
    return f"Exchange {exchange.audit_exchange_id}: Packets={len(exchange.audit_packet_refs)}, Health={exchange.health_status}"
