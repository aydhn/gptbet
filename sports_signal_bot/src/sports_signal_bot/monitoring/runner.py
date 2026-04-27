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
