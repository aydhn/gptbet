from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNSTABLE = "unstable"
    FAILING = "failing"
    QUARANTINED = "quarantined"
    DISABLED = "disabled"


class ProviderHealthRecord(BaseModel):
    provider_name: str
    last_success_time: Optional[datetime] = None
    recent_failure_count: int = 0
    timeout_count: int = 0
    schema_error_count: int = 0
    empty_payload_anomaly_count: int = 0
    fallback_usage_frequency: float = 0.0
    average_fetch_duration_ms: float = 0.0
    recent_stale_payload_count: int = 0
    status: HealthStatus = HealthStatus.HEALTHY
    updated_at: datetime = Field(default_factory=datetime.utcnow)


def build_provider_health_snapshot(provider_name: str) -> ProviderHealthRecord:
    return ProviderHealthRecord(provider_name=provider_name)


def detect_provider_instability(health: ProviderHealthRecord) -> bool:
    return health.recent_failure_count > 3 or health.timeout_count > 5


def classify_provider_health(health: ProviderHealthRecord) -> HealthStatus:
    if health.recent_failure_count > 10:
        return HealthStatus.QUARANTINED
    elif detect_provider_instability(health):
        return HealthStatus.UNSTABLE
    elif health.recent_failure_count > 0 or health.fallback_usage_frequency > 0.2:
        return HealthStatus.DEGRADED
    return HealthStatus.HEALTHY


def summarize_provider_failures(health: ProviderHealthRecord) -> Dict[str, int]:
    return {
        "failures": health.recent_failure_count,
        "timeouts": health.timeout_count,
        "schema_errors": health.schema_error_count,
        "anomalies": health.empty_payload_anomaly_count,
    }
