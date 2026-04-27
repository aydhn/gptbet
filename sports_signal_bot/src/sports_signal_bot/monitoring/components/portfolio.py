from typing import List, Dict, Any
from sports_signal_bot.monitoring.registry import HealthCheckRegistry
from sports_signal_bot.monitoring.checks import build_check_record
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthStatus, HealthSeverity

COMPONENT = "portfolio_health"

@HealthCheckRegistry.register(COMPONENT)
def check_portfolio_skip_rate(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    skip_rate = inputs.get("portfolio_skip_rate", 0.0)
    threshold = config.get("extreme_portfolio_skip_rate", 0.9)
    total_candidates = inputs.get("portfolio_candidates", 0)

    if skip_rate >= threshold and total_candidates > 0:
        status = HealthStatus.DEGRADED
        severity = HealthSeverity.WARNING
        msg = f"Extreme portfolio skip rate: {skip_rate:.2f} (threshold: {threshold})"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "Portfolio skip rate OK"

    checks.append(build_check_record(check_name="extreme_portfolio_skip_rate", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=skip_rate, threshold_reference=threshold))
    return checks
