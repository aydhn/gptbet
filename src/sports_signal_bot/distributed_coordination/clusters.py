import datetime
import uuid
from typing import List, Optional
from sports_signal_bot.distributed_coordination.contracts import (
    CoordinationClusterRecord,
    ClusterMembershipRecord
)

class CoordinationClusterManager:
    """Manages the lifecycle of a coordination cluster."""

    def build_cluster(self, cluster_name: str, cluster_family: str, tenancy_policy_ref: str) -> CoordinationClusterRecord:
        """Builds a new Coordination Cluster Record."""
        return CoordinationClusterRecord(
            cluster_id=f"cluster_{uuid.uuid4().hex[:8]}",
            cluster_name=cluster_name,
            cluster_family=cluster_family,
            member_node_refs=[],
            scheduler_pool_refs=[],
            broker_pool_refs=[],
            council_refs=[],
            tenancy_policy_ref=tenancy_policy_ref,
            active_status="active",
            warnings=[]
        )

    def join_cluster(self, cluster_ref: str, node_ref: str) -> ClusterMembershipRecord:
        """Records a node joining a cluster."""
        return ClusterMembershipRecord(
            cluster_ref=cluster_ref,
            node_ref=node_ref,
            joined_at=datetime.datetime.now(datetime.timezone.utc),
            status="active"
        )
