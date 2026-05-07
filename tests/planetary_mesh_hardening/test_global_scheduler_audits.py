from src.sports_signal_bot.planetary_mesh_hardening.scheduler_audits import build_global_continuity_scheduler_audit, summarize_global_scheduler_audit
from src.sports_signal_bot.planetary_mesh_hardening.contracts import AuditStatus

def test_global_scheduler_seam_gap():
    # 6) Global scheduler seam gap set
    audit = build_global_continuity_scheduler_audit("s_gap", "planetary_coverage_scheduler_audit")
    audit.seam_refs.append("seam")
    summarize_global_scheduler_audit(audit)
    assert audit.audit_status == AuditStatus.SCHEDULER_GAPPED
