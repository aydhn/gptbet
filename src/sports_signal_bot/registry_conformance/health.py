from datetime import datetime, timezone
from typing import Dict, List
from .contracts import CorridorRegistryRecord, RegistryHealthRecordV2


def detect_registry_currentness_issues(registry: CorridorRegistryRecord) -> List[str]:
    issues = []
    # In reality, we would load all actual entries referenced by `current_pointer_refs`
    # Here we simulate finding stale/superseded issues for health scoring
    if registry.health_status.stale_current_count > 0:
        issues.append(
            f"Found {registry.health_status.stale_current_count} stale current pointers."
        )
    if registry.health_status.expired_entry_misuse_pressure > 50:
        issues.append(
            f"High misuse pressure ({registry.health_status.expired_entry_misuse_pressure}%) from expired entries."
        )
    if registry.health_status.attestation_validity_coverage < 50:
        issues.append(
            f"Low attestation validity coverage ({registry.health_status.attestation_validity_coverage}%)."
        )

    return issues


def compute_registry_health(registry: CorridorRegistryRecord) -> CorridorRegistryRecord:
    now = datetime.now(timezone.utc)

    issues = detect_registry_currentness_issues(registry)

    status = "healthy"
    if len(issues) > 2:
        status = "degraded"
    elif len(issues) > 0:
        status = "caution"

    registry.health_status = RegistryHealthRecordV2(
        status=status,
        stale_current_count=registry.health_status.stale_current_count,
        expired_entry_misuse_pressure=registry.health_status.expired_entry_misuse_pressure,
        attestation_validity_coverage=registry.health_status.attestation_validity_coverage,
        last_evaluated_at=now,
    )

    return registry


def summarize_registry_health_drivers(registry: CorridorRegistryRecord) -> Dict:
    return {
        "status": registry.health_status.status,
        "stale_count": registry.health_status.stale_current_count,
        "misuse_pressure": registry.health_status.expired_entry_misuse_pressure,
        "validity_coverage": registry.health_status.attestation_validity_coverage,
    }


def downgrade_registry_health_on_gap_pressure(
    registry: CorridorRegistryRecord, gap_count: int
) -> CorridorRegistryRecord:
    if gap_count > 5:
        registry.health_status.status = "blocked"
        registry.warnings.append("Registry health blocked due to extreme gap pressure.")
    elif gap_count > 2 and registry.health_status.status in ["healthy", "caution"]:
        registry.health_status.status = "attestation_gap_heavy"
        registry.warnings.append("Registry health downgraded due to gap pressure.")
    return registry
