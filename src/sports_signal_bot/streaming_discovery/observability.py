from typing import List, Dict
from datetime import datetime
from .contracts import EcosystemHealthSnapshotRecord, SyncAnomalyClusterRecord, DegradationModeRecord

class ObservabilityFabric:
    def __init__(self):
        self.snapshots: List[EcosystemHealthSnapshotRecord] = []

    def capture_snapshot(self,
                         active_subs: int,
                         healthy_src: int,
                         degraded_src: int,
                         clusters: List[SyncAnomalyClusterRecord],
                         modes: List[DegradationModeRecord]) -> EcosystemHealthSnapshotRecord:

        cluster_counts = {"high": 0, "medium": 0, "low": 0}
        for c in clusters:
            if c.severity in cluster_counts:
                cluster_counts[c.severity] += 1

        is_degraded = any(m.mode_family != "normal_operation" and m.is_active for m in modes)
        status = "degraded" if is_degraded else "healthy"

        snapshot = EcosystemHealthSnapshotRecord(
            active_subscriptions=active_subs,
            healthy_sources=healthy_src,
            degraded_sources=degraded_src,
            stale_source_count=0,
            sync_lag_distribution={"p50": 0.0, "p99": 0.0},
            overlay_conflict_burden=0,
            anomaly_cluster_count_by_severity=cluster_counts,
            route_flip_rate=0.0,
            no_safe_route_incidents=0,
            quarantine_pressure=0.0,
            health_status=status
        )
        self.snapshots.append(snapshot)
        return snapshot
