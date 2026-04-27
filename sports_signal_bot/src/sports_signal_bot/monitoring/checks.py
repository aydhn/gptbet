from typing import List, Any
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthSeverity, HealthStatus

def build_check_record(check_name: str, component_name: str, run_id: str, status: HealthStatus, severity: HealthSeverity, message: str, measured_value: Any = None, threshold_reference: Any = None) -> HealthCheckRecord:
    return HealthCheckRecord(check_name=check_name, component_name=component_name, run_id=run_id, status=status, severity=severity, message=message, measured_value=measured_value, threshold_reference=threshold_reference)
