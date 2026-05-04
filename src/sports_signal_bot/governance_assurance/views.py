from typing import List
from sports_signal_bot.governance_assurance.contracts import (
    DashboardViewRecord,
    DashboardFamily
)

def create_dashboard_view(
    view_id: str,
    view_family: DashboardFamily,
    intended_audience: str,
    panel_refs: List[str]
) -> DashboardViewRecord:

    warnings = []
    if "no_safe_panel" not in panel_refs:
        warnings.append("missing_no_safe_visibility")

    return DashboardViewRecord(
        view_id=view_id,
        view_family=view_family,
        intended_audience=intended_audience,
        included_panel_refs=panel_refs,
        visibility_policy_ref="default_visibility",
        refresh_policy_ref="strict_refresh",
        currentness_state="current",
        warnings=warnings
    )
