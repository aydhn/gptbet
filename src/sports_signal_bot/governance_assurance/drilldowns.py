from typing import List
from sports_signal_bot.governance_assurance.contracts import (
    DashboardDrilldownRecord
)

def generate_drilldowns(target_refs: List[str]) -> List[DashboardDrilldownRecord]:
    drilldowns = []
    for i, ref in enumerate(target_refs):
        drilldowns.append(DashboardDrilldownRecord(
            drilldown_id=f"drilldown_{i}",
            target_ref=ref
        ))
    return drilldowns
