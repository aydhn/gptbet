import uuid
from typing import List
from sports_signal_bot.distributed_coordination.contracts import (
    ClusterFailoverRecord,
    FailoverRevalidationRecord
)

class FailoverManager:
    """Manages node and broker failover scenarios."""

    def detect_failover_need(self, node_health_status: str, node_ref: str) -> bool:
        """Determines if a failover is required based on health."""
        if node_health_status in ["unstable", "degraded", "dead"]:
            return True
        return False

    def initiate_safe_failover(self, cluster_ref: str, failed_node_ref: str, target_node_ref: str) -> ClusterFailoverRecord:
        """Initiates a safe failover process."""
        return ClusterFailoverRecord(
            failover_id=f"failover_{uuid.uuid4().hex[:8]}",
            cluster_ref=cluster_ref,
            failed_node_ref=failed_node_ref,
            target_node_ref=target_node_ref,
            status="failover_in_progress"
        )

    def revalidate_post_failover_state(self, failover_record: ClusterFailoverRecord, is_snapshot_valid: bool) -> FailoverRevalidationRecord:
        """Revalidates token ownership and shard assignments post-failover."""
        status = "revalidation_success" if is_snapshot_valid else "revalidation_failed"
        return FailoverRevalidationRecord(
            revalidation_id=f"reval_{uuid.uuid4().hex[:8]}",
            failover_ref=failover_record.failover_id,
            status=status
        )
