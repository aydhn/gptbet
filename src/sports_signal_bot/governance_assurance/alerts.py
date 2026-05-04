from typing import List
from sports_signal_bot.governance_assurance.contracts import (
    DashboardAlertRibbonRecord
)

def generate_alert_ribbons(conditions: List[str]) -> List[DashboardAlertRibbonRecord]:
    alerts = []
    for i, cond in enumerate(conditions):
        severity = "high" if "failure" in cond or "stale" in cond else "medium"
        alerts.append(DashboardAlertRibbonRecord(
            alert_id=f"alert_{i}",
            severity=severity,
            message=cond
        ))
    return alerts
