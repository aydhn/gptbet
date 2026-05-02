from typing import List, Dict
from datetime import datetime
from .contracts import DiscoveryEventRecord, SyncAnomalyClusterRecord

class AnomalyClusterer:
    def __init__(self):
        self.active_clusters: Dict[str, SyncAnomalyClusterRecord] = {}

    def process_event(self, event: DiscoveryEventRecord):
        # Simplistic heuristic: group consecutive failures by source
        if "fail" in event.event_family.lower() or "degrade" in event.event_family.lower() or "no_safe" in event.event_family.lower():
            cluster_key = f"{event.source_ref}_{event.event_family}"

            if cluster_key not in self.active_clusters:
                self.active_clusters[cluster_key] = SyncAnomalyClusterRecord(
                    cluster_family=f"likely_{event.event_family}_issue",
                    member_event_ids=[event.event_id],
                    suspected_root_causes=[f"Repeated {event.event_family} for source {event.source_ref}"],
                    affected_sources=[event.source_ref],
                    affected_routes=[],
                    severity="medium",
                    first_seen_at=event.event_time
                )
            else:
                cluster = self.active_clusters[cluster_key]
                if event.event_id not in cluster.member_event_ids:
                    cluster.member_event_ids.append(event.event_id)
                if len(cluster.member_event_ids) >= 3:
                    cluster.severity = "high"

    def get_clusters(self) -> List[SyncAnomalyClusterRecord]:
        return list(self.active_clusters.values())
