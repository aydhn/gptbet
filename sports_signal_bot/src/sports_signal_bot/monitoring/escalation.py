from typing import List, Dict, Optional
from sports_signal_bot.monitoring.contracts import (HealthAlertRecord, EscalationDecision, EscalationRecord, HealthSeverity)

class EscalationPolicy:
    def __init__(self, name: str, severity_map: Dict[HealthSeverity, str]):
        self.name = name
        self.severity_map = severity_map

def should_escalate(alert: HealthAlertRecord, policy: EscalationPolicy) -> bool:
    return alert.severity in policy.severity_map

def build_escalation_decision(alert: HealthAlertRecord, policy: EscalationPolicy) -> Optional[EscalationDecision]:
    if not should_escalate(alert, policy): return None
    action = "route_to_channel"
    escalate_to = policy.severity_map[alert.severity]
    return EscalationDecision(policy_name=policy.name, action=action, severity=alert.severity, escalate_to=escalate_to, reason=f"Severity {alert.severity.value} mapped to {escalate_to}")

def track_repeated_failures(alerts: List[HealthAlertRecord], history: List[List[HealthAlertRecord]]) -> List[HealthAlertRecord]:
    promoted_alerts = []
    if not history: return alerts
    last_run_alerts = {a.check_name: a for a in history[-1]}
    for alert in alerts:
        if alert.check_name in last_run_alerts:
            new_severity = alert.severity
            if alert.severity == HealthSeverity.WARNING: new_severity = HealthSeverity.ERROR
            elif alert.severity == HealthSeverity.ERROR: new_severity = HealthSeverity.CRITICAL

            if new_severity != alert.severity:
                new_alert = alert.copy(update={"severity": new_severity, "message": f"[ESCALATED] {alert.message}"})
                promoted_alerts.append(new_alert)
            else:
                promoted_alerts.append(alert)
        else:
            promoted_alerts.append(alert)
    return promoted_alerts

def classify_incident_candidate(alerts: List[HealthAlertRecord]) -> List[HealthAlertRecord]:
    return [a for a in alerts if a.severity == HealthSeverity.CRITICAL]

def generate_escalation_record(run_id: str, decisions: List[EscalationDecision]) -> EscalationRecord:
    highest_severity = HealthSeverity.INFO
    severity_rank = {HealthSeverity.INFO: 0, HealthSeverity.WARNING: 1, HealthSeverity.ERROR: 2, HealthSeverity.CRITICAL: 3}
    actions = []
    for decision in decisions:
        if severity_rank[decision.severity] > severity_rank[highest_severity]: highest_severity = decision.severity
        actions.append(f"{decision.action} -> {decision.escalate_to}")
    return EscalationRecord(run_id=run_id, alerts_escalated=len(decisions), highest_severity=highest_severity, actions_taken=list(set(actions)))
