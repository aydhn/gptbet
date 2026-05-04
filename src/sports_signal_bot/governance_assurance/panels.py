from typing import List
from sports_signal_bot.governance_assurance.contracts import (
    DashboardPanelRecord,
    PanelFamily
)

def create_dashboard_panel(
    panel_id: str,
    panel_family: PanelFamily,
    metric_refs: List[str]
) -> DashboardPanelRecord:
    return DashboardPanelRecord(
        panel_id=panel_id,
        panel_family=panel_family,
        metric_refs=metric_refs
    )
