from typing import List, Dict, Any, Optional
from uuid import uuid4
from sports_signal_bot.monitoring.contracts import (AnomalySignalRecord, HealthSeverity, HealthScoreRecord, ComponentHealthRecord)

class AnomalyRule:
    def __init__(self, name: str, threshold: Any, severity: HealthSeverity, suggested_escalation: str):
        self.name = name
        self.threshold = threshold
        self.severity = severity
        self.suggested_escalation = suggested_escalation

def classify_anomaly_severity(severity_str: str) -> HealthSeverity:
    try: return HealthSeverity(severity_str.lower())
    except ValueError: return HealthSeverity.WARNING

def build_anomaly_signals(run_id: str, rule: AnomalyRule, measured_value: Any, message: str) -> AnomalySignalRecord:
    return AnomalySignalRecord(anomaly_id=str(uuid4()), rule_name=rule.name, run_id=run_id, severity=rule.severity, measured_value=measured_value, baseline_threshold=rule.threshold, suggested_escalation=rule.suggested_escalation, message=message)

def summarize_anomaly_patterns(anomalies: List[AnomalySignalRecord]) -> Dict[HealthSeverity, int]:
    summary = {sev: 0 for sev in HealthSeverity}
    for anomaly in anomalies: summary[anomaly.severity] += 1
    return summary

def detect_run_anomalies(run_id: str, health_score: HealthScoreRecord, config_rules: Dict[str, dict]) -> List[AnomalySignalRecord]:
    anomalies = []
    if "low_health_score" in config_rules:
        rule_cfg = config_rules["low_health_score"]
        threshold = rule_cfg.get("threshold", 50.0)
        if health_score.global_score < threshold:
            rule = AnomalyRule("low_health_score", threshold, classify_anomaly_severity(rule_cfg.get("severity", "critical")), rule_cfg.get("escalation", "escalate_to_critical"))
            anomalies.append(build_anomaly_signals(run_id, rule, health_score.global_score, f"Global health score {health_score.global_score:.1f} is below threshold {threshold}"))

    inference_health = health_score.components.get("inference_health")
    if inference_health and "too_many_failed_steps" in config_rules:
        rule_cfg = config_rules["too_many_failed_steps"]
        threshold = rule_cfg.get("threshold", 2)
        if inference_health.failed_checks >= threshold:
            rule = AnomalyRule("too_many_failed_steps", threshold, classify_anomaly_severity(rule_cfg.get("severity", "error")), rule_cfg.get("escalation", "escalate_to_error"))
            anomalies.append(build_anomaly_signals(run_id, rule, inference_health.failed_checks, f"Inference health has {inference_health.failed_checks} failed checks (threshold: {threshold})"))
    return anomalies
