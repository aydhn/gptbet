import uuid
from typing import List, Dict, Any
from sports_signal_bot.execution_coordination.contracts import ContentionRecord, ContentionFamily, ContentionSeverity

class DistributedContentionManager:
    """Manages cross-node contention detection and clustering."""

    def detect_distributed_contentions(
        self,
        lane_ref: str,
        node_id: str,
        cluster_shared_surfaces: Dict[str, List[str]]
    ) -> List[ContentionRecord]:
        """Detects contentions across the cluster based on shared surfaces."""
        contentions = []
        for surface, active_nodes in cluster_shared_surfaces.items():
            if node_id in active_nodes and len(active_nodes) > 1:
                 contentions.append(
                     ContentionRecord(
                         contention_id=f"dist_contention_{uuid.uuid4().hex[:8]}",
                         contention_family=ContentionFamily.ROUTE_CACHE_SURFACE_CONTENTION, # Generic dist contention mapping
                         involved_lane_refs=[lane_ref],
                         shared_surface=surface,
                         severity=ContentionSeverity.HIGH,
                         current_resolution_state="detected_cross_node",
                         arbitration_ref=None,
                         warnings=["Cross-node contention detected."]
                     )
                 )
        return contentions

    def correlate_contentions_across_nodes(self, contentions: List[ContentionRecord]) -> Dict[str, List[ContentionRecord]]:
        """Groups contentions by shared surface across nodes."""
        grouped = {}
        for c in contentions:
            if c.shared_surface not in grouped:
                grouped[c.shared_surface] = []
            grouped[c.shared_surface].append(c)
        return grouped
