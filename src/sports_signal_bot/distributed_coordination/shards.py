import datetime
import uuid
from typing import List, Optional, Dict
from sports_signal_bot.distributed_coordination.contracts import (
    SchedulerShardRecord,
    ShardOwnershipRecord,
    ShardLoadRecord,
    ShardReassignmentRecord
)

class SchedulerShardManager:
    """Manages multi-lane scheduler shards."""

    def build_scheduler_shards(self, shard_family: str, count: int, assign_to_node_ref: str) -> List[SchedulerShardRecord]:
        """Builds a specified number of scheduler shards."""
        shards = []
        for _ in range(count):
            shard = SchedulerShardRecord(
                shard_id=f"shard_{uuid.uuid4().hex[:8]}",
                shard_family=shard_family,
                assigned_node_ref=assign_to_node_ref,
                load=0.0
            )
            shards.append(shard)
        return shards

    def assign_lane_to_shard(self, lane_ref: str, shards: List[SchedulerShardRecord]) -> SchedulerShardRecord:
        """Assigns a lane to the shard with the lowest load. Simplistic round-robin / load-balance."""
        if not shards:
            raise ValueError("No available shards for lane assignment.")
        target_shard = min(shards, key=lambda s: s.load)
        return target_shard

    def detect_cross_shard_conflicts(self, lane_ref: str, active_shard_assignments: Dict[str, str]) -> bool:
        """
        Returns True if the lane is active in another shard already.
        active_shard_assignments maps lane_ref -> shard_id.
        """
        return lane_ref in active_shard_assignments

    def summarize_shard_load(self, shard: SchedulerShardRecord, active_lanes: int, pending_lanes: int) -> ShardLoadRecord:
        """Creates a load summary record for the shard."""
        return ShardLoadRecord(
            shard_ref=shard.shard_id,
            active_lanes=active_lanes,
            pending_lanes=pending_lanes
        )
