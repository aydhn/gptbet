import pytest
from sports_signal_bot.continuity_verification_hardening.audit_pulse_councils import (
    build_audit_pulse_council,
    open_audit_pulse_council_case,
    collect_audit_pulse_council_evidence,
    resolve_audit_pulse_council_case,
    summarize_audit_pulse_council
)
from sports_signal_bot.continuity_verification_hardening.contracts import (
    AuditPulseCouncilFamily,
    AuditPulseCouncilStatus,
    AuditPulseCouncilCaseRecord,
    AuditPulseCouncilEvidenceRecord
)

def test_build_audit_pulse_council():
    council = build_audit_pulse_council("council_test", AuditPulseCouncilFamily.follow_the_sun_pulse_council)
    assert council.audit_pulse_council_id == "council_test"
    assert council.council_family == AuditPulseCouncilFamily.follow_the_sun_pulse_council
    assert council.council_status == AuditPulseCouncilStatus.council_gapped

def test_resolve_audit_pulse_council_case():
    council = build_audit_pulse_council("council_test", AuditPulseCouncilFamily.follow_the_sun_pulse_council)
    evidence = [
        AuditPulseCouncilEvidenceRecord(evidence_id="evidence_1", is_sufficient=True)
    ]
    resolved_council = resolve_audit_pulse_council_case(council, evidence)
    assert resolved_council.council_status == AuditPulseCouncilStatus.council_verified
