from typing import List, Dict, Any
from sports_signal_bot.monitoring.registry import HealthCheckRegistry
from sports_signal_bot.monitoring.checks import build_check_record
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthStatus, HealthSeverity

COMPONENT = "dispatch_health"

@HealthCheckRegistry.register(COMPONENT)
def check_dispatch_failure_rate(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    failure_rate = inputs.get("dispatch_failure_rate", 0.0)
    threshold = config.get("dispatch_failure_rate_threshold", 0.1)

    if failure_rate >= threshold:
        status = HealthStatus.FAILED
        severity = HealthSeverity.ERROR
        msg = f"Dispatch failure rate {failure_rate:.2f} exceeds threshold {threshold}"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "Dispatch failure rate OK"

    checks.append(build_check_record(check_name="dispatch_failure_rate", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=failure_rate, threshold_reference=threshold))
    return checks
