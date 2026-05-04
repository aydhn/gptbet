import uuid
from typing import List, Dict
from .contracts import SovereignGovernanceAssuranceDashboardRecordV2, DashboardViewRecordV2, DashboardSnapshotRecordV2, WarningRecord

def build_governance_assurance_dashboard_v2(dashboard_family: str) -> SovereignGovernanceAssuranceDashboardRecordV2:
    return SovereignGovernanceAssuranceDashboardRecordV2(
        dashboard_id=f"gad_{uuid.uuid4()}",
        dashboard_family=dashboard_family,
        view_refs=[],
        panel_refs=[],
        snapshot_refs=[],
        alert_refs=[],
        narrative_section_refs=[],
        audience_profile_refs=[],
        health_status="healthy",
        warnings=[]
    )

def create_dashboard_view_v2(intended_audience: str) -> DashboardViewRecordV2:
    return DashboardViewRecordV2(
        view_id=f"dv_{uuid.uuid4()}",
        view_family=f"{intended_audience}_view",
        intended_audience=intended_audience,
        included_panel_refs=[],
        included_narrative_refs=[],
        visibility_policy_ref="default_visibility",
        refresh_policy_ref="default_refresh",
        currentness_state="current",
        warnings=[]
    )

def capture_dashboard_snapshot_v2(dashboard: SovereignGovernanceAssuranceDashboardRecordV2, status: str = "snapshot_current") -> DashboardSnapshotRecordV2:
    snapshot = DashboardSnapshotRecordV2(
        snapshot_id=f"ds_{uuid.uuid4()}",
        status=status
    )
    dashboard.snapshot_refs.append(snapshot.snapshot_id)
    return snapshot

def summarize_dashboard_health_v2(dashboard: SovereignGovernanceAssuranceDashboardRecordV2) -> Dict:
    return {
        "id": dashboard.dashboard_id,
        "health": dashboard.health_status,
        "snapshots": len(dashboard.snapshot_refs),
        "views": len(dashboard.view_refs)
    }
