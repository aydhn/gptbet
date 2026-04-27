from typing import List, Dict, Any
from sports_signal_bot.monitoring.registry import HealthCheckRegistry
from sports_signal_bot.monitoring.checks import build_check_record
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthStatus, HealthSeverity

COMPONENT = "inference_health"

@HealthCheckRegistry.register(COMPONENT)
def check_event_universe(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    event_count = inputs.get("event_universe_size", 0)
    min_threshold = config.get("minimum_event_universe", 1)

    if event_count < min_threshold:
        status = HealthStatus.FAILED
        severity = HealthSeverity.ERROR
        msg = f"Empty or very small event universe: {event_count} (min: {min_threshold})"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = f"Event universe size OK ({event_count})"

    checks.append(build_check_record(check_name="event_universe_size", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=event_count, threshold_reference=min_threshold))
    return checks

@HealthCheckRegistry.register(COMPONENT)
def check_feature_build_failures(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    failure_count = inputs.get("feature_build_failures", 0)

    if failure_count > 0:
        status = HealthStatus.DEGRADED
        severity = HealthSeverity.WARNING
        msg = f"Feature build failures detected: {failure_count}"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "No feature build failures"

    checks.append(build_check_record(check_name="feature_build_failures", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=failure_count))
    return checks
