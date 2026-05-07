from typing import List
from .contracts import (
    GlobalAuditCadenceOrchestrationRecord, OrchestrationFamily, OrchestrationStatus,
    CadenceWindowRecord, GlobalAuditCadenceHealthRecord, GlobalAuditCadenceWarningRecord
)

def build_global_audit_cadence_orchestration(orch_id: str, family: OrchestrationFamily) -> GlobalAuditCadenceOrchestrationRecord:
    return GlobalAuditCadenceOrchestrationRecord(
        global_audit_cadence_orchestration_id=orch_id,
        orchestration_family=family
    )

def simulate_audit_cadence(orch: GlobalAuditCadenceOrchestrationRecord) -> GlobalAuditCadenceHealthRecord:
    stale_windows = [w for w in orch.window_refs if w.is_stale]
    missing_acks = [w for w in orch.window_refs if not w.has_ack]

    if missing_acks:
        orch.orchestration_status = OrchestrationStatus.ORCHESTRATION_BLOCKED
        orch.warnings.append(GlobalAuditCadenceWarningRecord(warning_id="blocked_cadence", description="Missing acks in cadence"))
        return GlobalAuditCadenceHealthRecord(is_healthy=False, status=OrchestrationStatus.ORCHESTRATION_BLOCKED)

    if stale_windows:
        orch.orchestration_status = OrchestrationStatus.ORCHESTRATION_CAVEATED
        orch.warnings.append(GlobalAuditCadenceWarningRecord(warning_id="stale_windows", description="Stale windows in cadence"))
        return GlobalAuditCadenceHealthRecord(is_healthy=False, status=OrchestrationStatus.ORCHESTRATION_CAVEATED)

    if not orch.window_refs:
        orch.orchestration_status = OrchestrationStatus.ORCHESTRATION_GAPPED
        return GlobalAuditCadenceHealthRecord(is_healthy=False, status=OrchestrationStatus.ORCHESTRATION_GAPPED)

    orch.orchestration_status = OrchestrationStatus.ORCHESTRATION_VERIFIED
    return GlobalAuditCadenceHealthRecord(is_healthy=True, status=OrchestrationStatus.ORCHESTRATION_VERIFIED)

def detect_cadence_gaps_and_seams(orch: GlobalAuditCadenceOrchestrationRecord) -> List[str]:
    issues = []
    if not orch.window_refs:
        issues.append("missing_windows")
    if not orch.zone_refs:
        issues.append("missing_zones")
    return issues

def summarize_global_audit_cadence(orch: GlobalAuditCadenceOrchestrationRecord) -> dict:
    return {
        "id": orch.global_audit_cadence_orchestration_id,
        "family": orch.orchestration_family.value,
        "status": orch.orchestration_status.value,
        "warnings_count": len(orch.warnings)
    }

def verify_cadence_handoff(orch: GlobalAuditCadenceOrchestrationRecord) -> bool:
    return orch.orchestration_status == OrchestrationStatus.ORCHESTRATION_VERIFIED

def validate_cadence_reachability(orch: GlobalAuditCadenceOrchestrationRecord) -> bool:
    return all(w.has_ack for w in orch.window_refs)

def detect_cadence_drifts_and_seams(orch: GlobalAuditCadenceOrchestrationRecord) -> List[str]:
    return detect_cadence_gaps_and_seams(orch)

def summarize_cadence_windows(windows: List[CadenceWindowRecord]) -> dict:
    return {
        "total": len(windows),
        "stale": sum(1 for w in windows if w.is_stale),
        "missing_ack": sum(1 for w in windows if not w.has_ack)
    }
