import uuid
from typing import List
from sports_signal_bot.distributed_coordination.contracts import CoordinationNodeRecord

class CoordinationNodeManager:
    """Manages coordination nodes."""

    def build_node(self, cluster_ref: str, roles: List[str]) -> CoordinationNodeRecord:
        """Builds a Coordination Node Record."""
        return CoordinationNodeRecord(
            node_id=f"node_{uuid.uuid4().hex[:8]}",
            cluster_ref=cluster_ref,
            roles=roles,
            active=True
        )
