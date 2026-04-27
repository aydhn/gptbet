from typing import List, Dict, Any
from sports_signal_bot.monitoring.registry import HealthCheckRegistry
from sports_signal_bot.monitoring.checks import build_check_record
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthStatus, HealthSeverity

COMPONENT = "decision_health"

@HealthCheckRegistry.register(COMPONENT)
def check_approved_count(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    approved_count = inputs.get("approved_count", -1)
    event_count = inputs.get("event_universe_size", 0)

    if approved_count == 0 and event_count > 0:
        status = HealthStatus.DEGRADED
        severity = HealthSeverity.WARNING
        msg = "Zero approved actions despite non-empty universe"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "Approved count OK"

    checks.append(build_check_record(check_name="zero_approved_count", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=approved_count))
    return checks

@HealthCheckRegistry.register(COMPONENT)
def check_no_action_ratio(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    no_action_count = inputs.get("no_action_count", 0)
    total_actions = inputs.get("total_actions", 1)

    ratio = no_action_count / max(total_actions, 1)
    threshold = config.get("no_action_ratio_warning_threshold", 0.95)

    if ratio >= threshold and total_actions > 5:
        status = HealthStatus.DEGRADED
        severity = HealthSeverity.WARNING
        msg = f"Unusually high no_action ratio: {ratio:.2f} (threshold: {threshold})"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "No-action ratio OK"

    checks.append(build_check_record(check_name="high_no_action_ratio", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=ratio, threshold_reference=threshold))
    return checks
