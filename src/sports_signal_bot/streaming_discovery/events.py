from enum import Enum

class EventFamily(str, Enum):
    SYNC_STARTED = "sync_started"
    SYNC_SUCCEEDED = "sync_succeeded"
    SYNC_PARTIAL = "sync_partial"
    SYNC_FAILED = "sync_failed"
    OVERLAY_BUILT = "overlay_built"
    ROUTE_SELECTED = "route_selected"
    ROUTE_DEGRADED = "route_degraded"
    TRUST_DOWNGRADED = "trust_downgraded"
    FRESHNESS_DEGRADED = "freshness_degraded"
    QUARANTINE_ENTERED = "quarantine_entered"
    NO_SAFE_ROUTE = "no_safe_route"
    ANOMALY_CLUSTER_OPENED = "anomaly_cluster_opened"
