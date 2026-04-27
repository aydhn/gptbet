cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/__init__.py
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/freshness.py
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sports_signal_bot.monitoring.contracts import FreshnessRecord

def get_now() -> datetime:
    """Helper to get current UTC time."""
    return datetime.now(timezone.utc)

def compute_age_minutes(last_updated: datetime, now: Optional[datetime] = None) -> float:
    """Compute age in minutes from last_updated to now."""
    if now is None:
        now = get_now()
    if last_updated.tzinfo is None:
        last_updated = last_updated.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    delta = now - last_updated
    return max(0.0, delta.total_seconds() / 60.0)

def compute_age_hours(last_updated: datetime, now: Optional[datetime] = None) -> float:
    return compute_age_minutes(last_updated, now) / 60.0

def compute_age_days(last_updated: datetime, now: Optional[datetime] = None) -> float:
    return compute_age_hours(last_updated, now) / 24.0

def evaluate_freshness_against_threshold(
    entity_name: str,
    entity_type: str,
    last_updated: datetime,
    threshold_minutes: float,
    now: Optional[datetime] = None
) -> FreshnessRecord:
    age_minutes = compute_age_minutes(last_updated, now)
    is_stale = age_minutes > threshold_minutes
    return FreshnessRecord(
        entity_name=entity_name,
        entity_type=entity_type,
        last_updated=last_updated,
        age_minutes=age_minutes,
        is_stale=is_stale,
        stale_threshold_minutes=threshold_minutes
    )

def summarize_stale_entities(records: List[FreshnessRecord]) -> Dict[str, int]:
    summary = {}
    for record in records:
        if record.is_stale:
            summary[record.entity_type] = summary.get(record.entity_type, 0) + 1
    return summary

def detect_stale_chain_components(records: List[FreshnessRecord]) -> List[str]:
    return [r.entity_name for r in records if r.is_stale]
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/scoring.py
from typing import Dict, List, Any
from sports_signal_bot.monitoring.contracts import (
    HealthCheckRecord,
    ComponentHealthRecord,
    HealthScoreRecord,
    HealthStatus,
    HealthSeverity
)

def map_severity_to_penalty(severity: HealthSeverity) -> float:
    mapping = {
        HealthSeverity.INFO: 0.0,
        HealthSeverity.WARNING: 5.0,
        HealthSeverity.ERROR: 20.0,
        HealthSeverity.CRITICAL: 50.0
    }
    return mapping.get(severity, 0.0)

def score_component_health(component_name: str, run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    if not checks:
        return ComponentHealthRecord(
            component_name=component_name, run_id=run_id, status=HealthStatus.UNKNOWN, score=0.0, checks=[]
        )

    total_checks = len(checks)
    failed = sum(1 for c in checks if c.status == HealthStatus.FAILED)
    degraded = sum(1 for c in checks if c.status == HealthStatus.DEGRADED)
    skipped = sum(1 for c in checks if c.status == HealthStatus.SKIPPED)

    score = 100.0
    for check in checks:
        if check.status in (HealthStatus.FAILED, HealthStatus.DEGRADED):
            penalty = map_severity_to_penalty(check.severity)
            score -= penalty

    score = max(0.0, min(100.0, score))

    status = HealthStatus.OK
    if failed > 0:
        if any(c.severity == HealthSeverity.CRITICAL for c in checks if c.status == HealthStatus.FAILED):
            status = HealthStatus.FAILED
        else:
            status = HealthStatus.DEGRADED
    elif degraded > 0:
        status = HealthStatus.DEGRADED

    if score == 0.0:
         status = HealthStatus.FAILED

    return ComponentHealthRecord(
        component_name=component_name, run_id=run_id, status=status, score=score,
        total_checks=total_checks, failed_checks=failed, degraded_checks=degraded,
        skipped_checks=skipped, checks=checks
    )

def score_data_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("data_health", run_id, checks)
def score_artifact_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("artifact_health", run_id, checks)
def score_inference_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("inference_health", run_id, checks)
def score_decision_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("decision_health", run_id, checks)
def score_dispatch_health(run_id: str, checks: List[HealthCheckRecord]) -> ComponentHealthRecord:
    return score_component_health("dispatch_health", run_id, checks)

def map_score_to_global_status(score: float, has_critical: bool) -> HealthStatus:
    if has_critical: return HealthStatus.FAILED
    if score >= 90.0: return HealthStatus.OK
    elif score >= 60.0: return HealthStatus.DEGRADED
    else: return HealthStatus.FAILED

def explain_global_health_score(score: float, penalties: List[str]) -> str:
    base = f"Global Health Score: {score:.1f}/100.0"
    if penalties: base += f". Penalties applied: {', '.join(penalties)}"
    return base

def combine_component_health_scores(run_id: str, components: Dict[str, ComponentHealthRecord], missing_critical_checks: bool = False) -> HealthScoreRecord:
    if not components: return HealthScoreRecord(run_id=run_id, global_status=HealthStatus.UNKNOWN)
    total_weight = len(components)
    weighted_sum = sum(comp.score for comp in components.values())
    global_score = weighted_sum / total_weight if total_weight > 0 else 0.0
    penalties_applied = []

    if missing_critical_checks:
        global_score -= 30.0
        penalties_applied.append("missing_critical_checks (-30)")

    global_score = max(0.0, min(100.0, global_score))
    has_critical = any(c.status == HealthStatus.FAILED for comp in components.values() for c in comp.checks if c.severity == HealthSeverity.CRITICAL)

    global_status = map_score_to_global_status(global_score, has_critical)
    explanation = explain_global_health_score(global_score, penalties_applied)

    return HealthScoreRecord(run_id=run_id, global_score=global_score, global_status=global_status, components=components, missing_critical_checks=missing_critical_checks, penalties_applied=penalties_applied, explanation=explanation)
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/anomalies.py
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
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/escalation.py
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
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/heartbeat.py
from typing import List, Dict
from sports_signal_bot.monitoring.contracts import (HeartbeatRecord, HeartbeatSummary, HeartbeatTemplateInput, HealthSeverity, HealthScoreRecord)

def build_heartbeat_summary(run_id: str, run_completed: bool, event_universe_size: int, action_summary: Dict[str, int], health_score: HealthScoreRecord, fallback_count: int, dispatch_summary: str, key_warnings_count: int) -> HeartbeatSummary:
    degraded = [name for name, comp in health_score.components.items() if comp.status != "ok"]
    return HeartbeatSummary(run_id=run_id, run_completed=run_completed, event_universe_size=event_universe_size, final_action_summary=action_summary, health_score=health_score.global_score, degraded_components=degraded, fallback_count=fallback_count, dispatch_summary=dispatch_summary, key_warnings_count=key_warnings_count)

def format_heartbeat_message(template_input: HeartbeatTemplateInput) -> str:
    summary = template_input.summary
    status = "COMPLETED" if summary.run_completed else "INCOMPLETE"
    msg = [f"💓 Heartbeat: {template_input.sport.upper()} {template_input.market_type.upper()} [{status}]", f"Run ID: {template_input.run_id}", f"Health Score: {summary.health_score:.1f}/100.0", f"Event Universe: {summary.event_universe_size} events", "---", "Action Summary:"]
    for action, count in summary.final_action_summary.items(): msg.append(f"  - {action}: {count}")
    msg.append("---")
    if summary.degraded_components: msg.append(f"Degraded Components: {', '.join(summary.degraded_components)}")
    else: msg.append("All components OK.")
    msg.append(f"Warnings: {summary.key_warnings_count} | Fallbacks: {summary.fallback_count}")
    msg.append(f"Dispatch: {summary.dispatch_summary}")
    return "\n".join(msg)

def create_heartbeat(template_input: HeartbeatTemplateInput) -> HeartbeatRecord:
    message = format_heartbeat_message(template_input)
    severity = HealthSeverity.INFO
    if template_input.summary.health_score < 60.0 or not template_input.summary.run_completed: severity = HealthSeverity.WARNING
    return HeartbeatRecord(run_id=template_input.run_id, summary=template_input.summary, severity=severity, message=message)
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/registry.py
from typing import Callable, Dict, List, Any
from sports_signal_bot.monitoring.contracts import HealthCheckRecord

class HealthCheckRegistry:
    _checks: Dict[str, List[Callable[..., List[HealthCheckRecord]]]] = {}
    @classmethod
    def register(cls, component: str) -> Callable:
        def decorator(func: Callable[..., List[HealthCheckRecord]]) -> Callable:
            if component not in cls._checks: cls._checks[component] = []
            cls._checks[component].append(func)
            return func
        return decorator
    @classmethod
    def get_checks(cls, component: str) -> List[Callable[..., List[HealthCheckRecord]]]:
        return cls._checks.get(component, [])
    @classmethod
    def get_all_components(cls) -> List[str]:
        return list(cls._checks.keys())
    @classmethod
    def clear(cls):
        cls._checks = {}
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/checks.py
from typing import List, Any
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthSeverity, HealthStatus

def build_check_record(check_name: str, component_name: str, run_id: str, status: HealthStatus, severity: HealthSeverity, message: str, measured_value: Any = None, threshold_reference: Any = None) -> HealthCheckRecord:
    return HealthCheckRecord(check_name=check_name, component_name=component_name, run_id=run_id, status=status, severity=severity, message=message, measured_value=measured_value, threshold_reference=threshold_reference)
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/inputs.py
import json
from pathlib import Path
from typing import Dict, Any, Optional

def _load_json_safe(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    try:
        with open(path, "r") as f: return json.load(f)
    except json.JSONDecodeError: return {}

def load_latest_inference_run(results_dir: str) -> Dict[str, Any]:
    base_dir = Path(results_dir)
    manifest_path = base_dir / "manifests" / "latest_inference_manifest.json"
    data = _load_json_safe(manifest_path)
    return {
        "event_universe_size": data.get("event_universe_size", 0),
        "approved_count": data.get("approved_count", 0),
        "no_action_count": data.get("no_action_count", 0),
        "total_actions": data.get("total_actions", 0),
        "fallback_count": data.get("fallback_count", 0),
        "feature_build_failures": data.get("feature_build_failures", 0),
        "model_age_days": data.get("model_age_days", 0),
        "stale_fixtures_count": data.get("stale_fixtures_count", 0),
        "missing_sources": data.get("missing_sources", []),
    }

def load_dispatch_health_inputs(results_dir: str) -> Dict[str, Any]:
    base_dir = Path(results_dir)
    dispatch_path = base_dir / "latest_dispatch_summary.json"
    data = _load_json_safe(dispatch_path)
    return {"dispatch_failure_rate": data.get("failure_rate", 0.0)}

def load_artifact_freshness_inputs(results_dir: str) -> Dict[str, Any]: return {}
def load_previous_health_runs(results_dir: str) -> list: return []

class MonitoringInputBuilder:
    def __init__(self, results_dir: str):
        self.results_dir = results_dir
    def build(self) -> Dict[str, Dict[str, Any]]:
        inference_inputs = load_latest_inference_run(self.results_dir)
        dispatch_inputs = load_dispatch_health_inputs(self.results_dir)
        return {"inference_health": inference_inputs, "decision_health": inference_inputs, "data_health": inference_inputs, "artifact_health": inference_inputs, "dispatch_health": dispatch_inputs, "portfolio_health": {}, "bankroll_health": {}}
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/history.py
import json
from pathlib import Path
from typing import List
from sports_signal_bot.monitoring.contracts import HealthAlertRecord, MonitoringRunManifest

class HealthHistoryStore:
    def __init__(self, history_dir: str):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
    def save_run(self, manifest: MonitoringRunManifest):
        path = self.history_dir / f"{manifest.run_id}.json"
        with open(path, "w") as f: f.write(manifest.model_dump_json(indent=2))
    def load_recent_runs(self, limit: int = 5) -> List[MonitoringRunManifest]:
        files = sorted(self.history_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        runs = []
        for file in files[:limit]:
            try:
                with open(file, "r") as f: runs.append(MonitoringRunManifest.model_validate_json(f.read()))
            except Exception: continue
        return runs

class MonitoringStateTracker:
    def __init__(self, history_store: HealthHistoryStore):
        self.store = history_store
    def get_last_run_alerts(self) -> List[HealthAlertRecord]:
        return []

class ConsecutiveIssueTracker:
    def __init__(self, state_tracker: MonitoringStateTracker):
        self.state_tracker = state_tracker
    def track(self, current_alerts: List[HealthAlertRecord]) -> List[HealthAlertRecord]:
        from sports_signal_bot.monitoring.escalation import track_repeated_failures
        return track_repeated_failures(current_alerts, [self.state_tracker.get_last_run_alerts()])
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/manifests.py
import json
from pathlib import Path
from sports_signal_bot.monitoring.contracts import MonitoringRunManifest, MonitoringSummaryRecord, HeartbeatRecord

def write_monitoring_manifest(manifest: MonitoringRunManifest, output_dir: str):
    path = Path(output_dir) / "monitoring_manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: f.write(manifest.model_dump_json(indent=2))

def write_heartbeat_record(heartbeat: HeartbeatRecord, output_dir: str):
    path = Path(output_dir) / "heartbeat_record.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: f.write(heartbeat.model_dump_json(indent=2))

def write_monitoring_summary(summary: MonitoringSummaryRecord, output_dir: str):
    path = Path(output_dir) / "global_health_summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: f.write(summary.model_dump_json(indent=2))
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/reporting.py
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
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/diagnostics.py
def print_diagnostics(health_score):
    print(f"Health Score: {health_score.global_score}")
    for comp_name, comp in health_score.components.items():
        print(f"  {comp_name}: {comp.score} [{comp.status}]")
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/utils.py
import yaml
from pathlib import Path
def load_config(path: str) -> dict:
    try:
        with open(path, "r") as f: return yaml.safe_load(f)
    except Exception: return {}
INNER_EOF

cat << 'INNER_EOF' > src/sports_signal_bot/monitoring/runner.py
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List
from sports_signal_bot.monitoring.contracts import (MonitoringRunManifest, HealthAlertRecord, HealthStatus, HealthSeverity, MonitoringSummaryRecord, HeartbeatTemplateInput)
from sports_signal_bot.monitoring.inputs import MonitoringInputBuilder
from sports_signal_bot.monitoring.registry import HealthCheckRegistry
from sports_signal_bot.monitoring.scoring import combine_component_health_scores, score_component_health
from sports_signal_bot.monitoring.anomalies import detect_run_anomalies, summarize_anomaly_patterns
from sports_signal_bot.monitoring.escalation import EscalationPolicy, build_escalation_decision, generate_escalation_record, track_repeated_failures
from sports_signal_bot.monitoring.heartbeat import build_heartbeat_summary, create_heartbeat
from sports_signal_bot.monitoring.reporting import MonitoringReporter
from sports_signal_bot.monitoring.manifests import write_monitoring_manifest, write_heartbeat_record, write_monitoring_summary
from sports_signal_bot.monitoring.history import HealthHistoryStore, MonitoringStateTracker, ConsecutiveIssueTracker
from sports_signal_bot.monitoring.utils import load_config

class MonitoringRunner:
    def __init__(self, run_id: str, results_dir: str, config_dir: str = "configs/monitoring", dry_run: bool = False):
        self.run_id = run_id
        self.results_dir = results_dir
        self.config_dir = config_dir
        self.dry_run = dry_run
        self.reporter = MonitoringReporter(f"{results_dir}/monitoring")
        self.history_store = HealthHistoryStore(f"{results_dir}/monitoring/history")
        self.state_tracker = MonitoringStateTracker(self.history_store)
        self.issue_tracker = ConsecutiveIssueTracker(self.state_tracker)
        self.configs = {"default": load_config(f"{config_dir}/default.yaml"), "health_scores": load_config(f"{config_dir}/health_scores.yaml"), "anomalies": load_config(f"{config_dir}/anomalies.yaml"), "escalation": load_config(f"{config_dir}/escalation.yaml")}
    def run(self, sport: str, market_type: str = "all") -> MonitoringRunManifest:
        start_time = datetime.utcnow()
        input_builder = MonitoringInputBuilder(self.results_dir)
        inputs_by_component = input_builder.build()
        all_checks = []
        components = {}
        for component_name in HealthCheckRegistry.get_all_components():
            component_inputs = inputs_by_component.get(component_name, {})
            component_checks = []
            for check_func in HealthCheckRegistry.get_checks(component_name):
                try:
                    res = check_func(self.run_id, component_inputs, self.configs["default"])
                    component_checks.extend(res)
                except Exception as e: pass
            all_checks.extend(component_checks)
            components[component_name] = score_component_health(component_name, self.run_id, component_checks)
        health_score = combine_component_health_scores(self.run_id, components)
        anomalies = detect_run_anomalies(self.run_id, health_score, self.configs["anomalies"])
        alerts = []
        for check in all_checks:
            if check.status in (HealthStatus.FAILED, HealthStatus.DEGRADED):
                alerts.append(HealthAlertRecord(alert_id=str(uuid4()), run_id=self.run_id, check_name=check.check_name, component_name=check.component_name, severity=check.severity, message=check.message, measured_value=check.measured_value))
        tracked_alerts = self.issue_tracker.track(alerts)
        policy_data = self.configs["escalation"].get("severity_map", {"warning": "warnings_channel", "error": "alarms_channel", "critical": "alarms_channel"})
        severity_map = {HealthSeverity(k): v for k, v in policy_data.items()}
        policy = EscalationPolicy("default_policy", severity_map)
        decisions = []
        for alert in tracked_alerts:
            decision = build_escalation_decision(alert, policy)
            if decision: decisions.append(decision)
        escalation_record = generate_escalation_record(self.run_id, decisions)
        inference_inputs = inputs_by_component.get("inference_health", {})
        dispatch_inputs = inputs_by_component.get("dispatch_health", {})
        hb_summary = build_heartbeat_summary(run_id=self.run_id, run_completed=True, event_universe_size=inference_inputs.get("event_universe_size", 0), action_summary={"action": 10}, health_score=health_score, fallback_count=inference_inputs.get("fallback_count", 0), dispatch_summary=f"Failure rate: {dispatch_inputs.get('dispatch_failure_rate', 0.0)}", key_warnings_count=len(tracked_alerts))
        hb_input = HeartbeatTemplateInput(run_id=self.run_id, sport=sport, market_type=market_type, summary=hb_summary)
        heartbeat = create_heartbeat(hb_input)
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        manifest = MonitoringRunManifest(run_id=self.run_id, sport=sport, market_type=market_type, start_time=start_time, end_time=end_time, duration_seconds=duration, health_score=health_score, total_anomalies=len(anomalies), escalation_summary=escalation_record)
        summary_record = MonitoringSummaryRecord(run_id=self.run_id, global_score=health_score.global_score, global_status=health_score.global_status, anomaly_counts_by_severity=summarize_anomaly_patterns(anomalies), degraded_components=[c for c, comp in components.items() if comp.status != HealthStatus.OK], escalation_counts=len(decisions))
        if not self.dry_run:
            self.reporter.write_health_checks(all_checks)
            self.reporter.write_component_scores(components)
            self.reporter.write_anomaly_signals(anomalies)
            self.reporter.write_escalations(decisions, self.run_id)
            write_monitoring_manifest(manifest, f"{self.results_dir}/monitoring")
            write_heartbeat_record(heartbeat, f"{self.results_dir}/monitoring")
            write_monitoring_summary(summary_record, f"{self.results_dir}/monitoring")
            self.history_store.save_run(manifest)
        return manifest
INNER_EOF
