from typing import List, Dict, Any
from sports_signal_bot.monitoring.registry import HealthCheckRegistry
from sports_signal_bot.monitoring.checks import build_check_record
from sports_signal_bot.monitoring.contracts import HealthCheckRecord, HealthStatus, HealthSeverity

COMPONENT = "data_health"

@HealthCheckRegistry.register(COMPONENT)
def check_fixture_freshness(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    stale_count = inputs.get("stale_fixtures_count", 0)
    threshold = config.get("stale_fixtures_threshold", 5)

    if stale_count > threshold:
        status = HealthStatus.DEGRADED
        severity = HealthSeverity.WARNING
        msg = f"{stale_count} stale fixtures found (threshold {threshold})"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "Fixture freshness OK"

    checks.append(build_check_record(check_name="fixture_freshness", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=stale_count, threshold_reference=threshold))
    return checks

@HealthCheckRegistry.register(COMPONENT)
def check_missing_sources(run_id: str, inputs: Dict[str, Any], config: Dict[str, Any]) -> List[HealthCheckRecord]:
    checks = []
    missing_sources = inputs.get("missing_sources", [])

    if missing_sources:
        status = HealthStatus.FAILED
        severity = HealthSeverity.ERROR
        msg = f"Missing critical sources: {', '.join(missing_sources)}"
    else:
        status = HealthStatus.OK
        severity = HealthSeverity.INFO
        msg = "All required sources present"

    checks.append(build_check_record(check_name="missing_critical_sources", component_name=COMPONENT, run_id=run_id, status=status, severity=severity, message=msg, measured_value=len(missing_sources)))
    return checks
