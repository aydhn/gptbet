from typing import List, Dict, Any
from sports_signal_bot.governance_assurance.contracts import (
    SovereignGovernanceAssuranceDashboardRecord,
    DashboardFamily,
    GovernanceAssuranceDashboardWarningRecord
)

def build_governance_assurance_dashboard(
    dashboard_id: str,
    family: DashboardFamily
) -> SovereignGovernanceAssuranceDashboardRecord:
    return SovereignGovernanceAssuranceDashboardRecord(
        dashboard_id=dashboard_id,
        dashboard_family=family,
        view_refs=[],
        panel_refs=[],
        audience_profile_refs=[],
        snapshot_refs=[],
        alert_refs=[],
        health_status="healthy",
        warnings=[]
    )

def summarize_dashboard_health(dashboard: SovereignGovernanceAssuranceDashboardRecord) -> Dict[str, Any]:
    return {
        "dashboard_id": dashboard.dashboard_id,
        "family": dashboard.dashboard_family.value,
        "views": len(dashboard.view_refs),
        "snapshots": len(dashboard.snapshot_refs),
        "alerts": len(dashboard.alert_refs),
        "health": dashboard.health_status
    }
