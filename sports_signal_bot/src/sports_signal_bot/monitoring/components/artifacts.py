from sports_signal_bot.schema_governance.adapters import VersionedLoader, ContractAdapter
from sports_signal_bot.schema_governance.registry import SchemaRegistry
from typing import List, Dict, Any
from sports_signal_bot.monitoring.registry import HealthCheckRegistry
from sports_signal_bot.monitoring.checks import build_check_record
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthStatus, HealthSeverity

COMPONENT = "artifact_health"

@HealthCheckRegistry.register(COMPONENT)
def check_model_age(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    model_age_days = inputs.get("model_age_days", 0)
    threshold = config.get("max_model_age_days", 30)

    if model_age_days > threshold:
        status = HealthStatus.DEGRADED
        severity = HealthSeverity.WARNING
        msg = f"Model artifact is {model_age_days} days old (threshold: {threshold})"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "Model artifact age OK"

    checks.append(build_check_record(check_name="model_age", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=model_age_days, threshold_reference=threshold))
    return checks

@HealthCheckRegistry.register(COMPONENT)
def check_fallback_usage(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    fallback_count = inputs.get("fallback_count", 0)
    threshold = config.get("maximum_fallback_rate", 10)

    if fallback_count > threshold:
        status = HealthStatus.FAILED
        severity = HealthSeverity.ERROR
        msg = f"Repeated fallback usage: {fallback_count} times (threshold: {threshold})"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "Fallback usage OK"

    checks.append(build_check_record(check_name="repeated_fallback_usage", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=fallback_count, threshold_reference=threshold))
    return checks
