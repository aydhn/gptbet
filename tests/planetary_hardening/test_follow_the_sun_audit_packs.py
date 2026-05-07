import pytest
from src.sports_signal_bot.planetary_hardening.follow_the_sun_audits import (
    build_follow_the_sun_audit_pack,
    verify_follow_the_sun_audit_pack,
    verify_follow_the_sun_handoff
)
from src.sports_signal_bot.planetary_hardening.contracts import (
    AuditPackEvidenceRecord,
    AuditPackHandoffRecord
)

def test_build_follow_the_sun_audit_pack():
    audit = build_follow_the_sun_audit_pack("test_audit", [AuditPackEvidenceRecord(evidence_id="e1")])
    assert audit.audit_family == "test_audit"

def test_verify_follow_the_sun_audit_pack_fresh():
    audit = build_follow_the_sun_audit_pack("test_audit", [AuditPackEvidenceRecord(evidence_id="e1", is_stale=False)])
    audit = verify_follow_the_sun_audit_pack(audit)
    # Gaps will make it gapped since we have no handoffs
    assert audit.audit_status == "audit_gapped"

def test_verify_follow_the_sun_audit_pack_with_handoff():
    audit = build_follow_the_sun_audit_pack("test_audit", [AuditPackEvidenceRecord(evidence_id="e1", is_stale=False)])
    audit = verify_follow_the_sun_handoff(audit, AuditPackHandoffRecord(handoff_id="h1", is_replayable=True))
    audit = verify_follow_the_sun_audit_pack(audit)
    assert audit.audit_status == "audit_verified"

def test_verify_follow_the_sun_handoff_unreplayable():
    audit = build_follow_the_sun_audit_pack("test_audit", [AuditPackEvidenceRecord(evidence_id="e1", is_stale=False)])
    audit = verify_follow_the_sun_handoff(audit, AuditPackHandoffRecord(handoff_id="h1", is_replayable=False))
    assert audit.audit_status == "audit_caveated"
