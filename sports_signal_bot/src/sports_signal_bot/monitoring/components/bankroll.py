from typing import List, Dict, Any
from sports_signal_bot.monitoring.registry import HealthCheckRegistry
from sports_signal_bot.monitoring.checks import build_check_record
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthStatus, HealthSeverity

COMPONENT = "bankroll_health"

@HealthCheckRegistry.register(COMPONENT)
def check_capital_curve_collapse(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    status = HealthStatus.OK
    severity = HealthSeverity.INFO
    msg = "Capital curve OK (Placeholder)"

    checks.append(build_check_record(check_name="capital_curve_collapse", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg))
    return checks
