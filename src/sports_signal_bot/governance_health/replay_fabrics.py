import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    LineageReplayFabricRecord,
    ReplayFabricNodeRecord,
    ReplayFabricChannelRecord
)

def build_lineage_replay_fabric(
    fabric_family: str,
    replay_policy_ref: str,
    pressure_policy_ref: str
) -> LineageReplayFabricRecord:
    return LineageReplayFabricRecord(
        replay_fabric_id=f"rfab_{uuid.uuid4().hex[:8]}",
        fabric_family=fabric_family, # type: ignore
        replay_policy_ref=replay_policy_ref,
        pressure_policy_ref=pressure_policy_ref,
        health_status="initializing"
    )

def add_replay_fabric_node(
    fabric: LineageReplayFabricRecord,
    node_family: str,
    replay_capacity: int,
    supported_lineage_families: List[str]
) -> ReplayFabricNodeRecord:
    node = ReplayFabricNodeRecord(
        node_id=f"rf_node_{uuid.uuid4().hex[:8]}",
        node_family=node_family, # type: ignore
        supported_lineage_families=supported_lineage_families,
        replay_capacity=replay_capacity,
        replay_load=0,
        currentness_state="current",
        node_status="active"
    )
    fabric.node_refs.append(node.node_id)
    return node

def add_replay_fabric_channel(
    fabric: LineageReplayFabricRecord,
    source_node_ref: str,
    target_node_ref: str,
    caveat_transfer_policy: str,
    replay_integrity_policy_ref: str
) -> ReplayFabricChannelRecord:
    channel = ReplayFabricChannelRecord(
        channel_id=f"rf_chan_{uuid.uuid4().hex[:8]}",
        source_node_ref=source_node_ref,
        target_node_ref=target_node_ref,
        caveat_transfer_policy=caveat_transfer_policy,
        replay_integrity_policy_ref=replay_integrity_policy_ref,
        channel_status="active"
    )
    fabric.channel_refs.append(channel.channel_id)
    return channel

def validate_replay_fabric_channel(channel: ReplayFabricChannelRecord, nodes: Dict[str, ReplayFabricNodeRecord]) -> bool:
    if channel.source_node_ref not in nodes or channel.target_node_ref not in nodes:
        channel.warnings.append("Channel references missing nodes")
        channel.channel_status = "blocked"
        return False

    source_node = nodes[channel.source_node_ref]
    target_node = nodes[channel.target_node_ref]

    if source_node.node_status != "active" or target_node.node_status != "active":
        channel.warnings.append("Channel references inactive nodes")
        channel.channel_status = "degraded"
        return False

    return True

def summarize_replay_fabric(
    fabric: LineageReplayFabricRecord,
    nodes: List[ReplayFabricNodeRecord],
    channels: List[ReplayFabricChannelRecord]
) -> Dict[str, Any]:

    total_capacity = sum(n.replay_capacity for n in nodes)
    total_load = sum(n.replay_load for n in nodes)

    degraded_channels = sum(1 for c in channels if c.channel_status != "active")

    if total_load > total_capacity * 0.9:
        health = "backpressured"
    elif degraded_channels > 0:
        health = "degraded"
    else:
        health = "healthy"

    fabric.health_status = health

    return {
        "fabric_id": fabric.replay_fabric_id,
        "family": fabric.fabric_family,
        "nodes": len(nodes),
        "channels": len(channels),
        "total_capacity": total_capacity,
        "total_load": total_load,
        "health_status": health,
        "degraded_channels": degraded_channels
    }
