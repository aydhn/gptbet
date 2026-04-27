import csv
from pathlib import Path
from typing import List, Dict, Any
from sports_signal_bot.monitoring.contracts import (HealthCheckRecord, ComponentHealthRecord, AnomalySignalRecord, EscalationDecision)

class MonitoringReporter:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    def write_health_checks(self, checks: List[HealthCheckRecord]):
        path = self.output_dir / "health_checks.csv"
        if not checks: return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["run_id", "component_name", "check_name", "status", "severity", "measured_value", "message", "created_at"])
            writer.writeheader()
            for check in checks: writer.writerow({"run_id": check.run_id, "component_name": check.component_name, "check_name": check.check_name, "status": check.status.value, "severity": check.severity.value, "measured_value": str(check.measured_value), "message": check.message, "created_at": check.created_at.isoformat()})
    def write_component_scores(self, components: Dict[str, ComponentHealthRecord]):
        path = self.output_dir / "component_health_scores.csv"
        if not components: return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["run_id", "component_name", "status", "score", "total_checks", "failed_checks"])
            writer.writeheader()
            for comp in components.values(): writer.writerow({"run_id": comp.run_id, "component_name": comp.component_name, "status": comp.status.value, "score": f"{comp.score:.1f}", "total_checks": comp.total_checks, "failed_checks": comp.failed_checks})
    def write_anomaly_signals(self, anomalies: List[AnomalySignalRecord]):
        path = self.output_dir / "anomaly_signals.csv"
        if not anomalies: return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["anomaly_id", "run_id", "rule_name", "severity", "measured_value", "suggested_escalation", "message"])
            writer.writeheader()
            for a in anomalies: writer.writerow({"anomaly_id": a.anomaly_id, "run_id": a.run_id, "rule_name": a.rule_name, "severity": a.severity.value, "measured_value": str(a.measured_value), "suggested_escalation": a.suggested_escalation, "message": a.message})
    def write_escalations(self, decisions: List[EscalationDecision], run_id: str):
        path = self.output_dir / "escalation_decisions.csv"
        if not decisions: return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["run_id", "policy_name", "action", "severity", "escalate_to", "reason"])
            writer.writeheader()
            for d in decisions: writer.writerow({"run_id": run_id, "policy_name": d.policy_name, "action": d.action, "severity": d.severity.value, "escalate_to": d.escalate_to, "reason": d.reason})
