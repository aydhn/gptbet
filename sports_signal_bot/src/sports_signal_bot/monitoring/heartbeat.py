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
