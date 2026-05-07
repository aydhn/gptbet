from typing import List
from .contracts import (
    CrossRegionRecoveryGovernanceRecord,
    GovernanceRegionRoleRecord,
    GovernanceDecisionWindowRecord,
    GovernanceApprovalRecord,
    GovernanceGapRecord,
    CrossRegionGovernanceWarningRecord
)

def build_cross_region_recovery_governance(governance_id: str, family: str) -> CrossRegionRecoveryGovernanceRecord:
    return CrossRegionRecoveryGovernanceRecord(
        cross_region_recovery_governance_id=governance_id,
        governance_family=family,
        governance_status="governance_verified"
    )

def register_governance_region_role(gov: CrossRegionRecoveryGovernanceRecord, role: GovernanceRegionRoleRecord) -> None:
    gov.region_role_refs.append(role)

def validate_governance_decision_windows(gov: CrossRegionRecoveryGovernanceRecord, window: GovernanceDecisionWindowRecord) -> None:
    gov.decision_window_refs.append(window)

def detect_cross_region_governance_gaps(gov: CrossRegionRecoveryGovernanceRecord, gap: GovernanceGapRecord) -> None:
    gov.gap_refs.append(gap)
    gov.governance_status = "governance_gapped"
    gov.warnings.append(CrossRegionGovernanceWarningRecord(
        warning_id=f"gap_{gap.gap_id}",
        message="ambiguous approval chain gap"
    ))

def summarize_cross_region_governance(gov: CrossRegionRecoveryGovernanceRecord) -> dict:
    return {
        "id": gov.cross_region_recovery_governance_id,
        "status": gov.governance_status,
        "roles_count": len(gov.region_role_refs),
        "windows_count": len(gov.decision_window_refs),
        "gaps_count": len(gov.gap_refs),
        "warnings": len(gov.warnings)
    }

def verify_governance_approval_path(gov: CrossRegionRecoveryGovernanceRecord, approval: GovernanceApprovalRecord) -> None:
    if approval.status == "missing_ack":
        gov.governance_status = "governance_caveated"
    gov.approval_refs.append(approval)
