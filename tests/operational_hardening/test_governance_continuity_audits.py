from sports_signal_bot.operational_hardening.continuity_audits import build_governance_continuity_audit

def test_build_governance_continuity_audit():
    audit = build_governance_continuity_audit("trace_continuity_audit")
    assert audit.audit_family == "trace_continuity_audit"
    assert audit.audit_status == "continuity_verified"
