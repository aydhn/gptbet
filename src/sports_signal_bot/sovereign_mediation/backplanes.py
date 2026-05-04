import uuid
from typing import List
from .contracts import SignalRoutingBackplaneRecord, BackplaneChannelRecord

def build_signal_routing_backplane(family: str) -> SignalRoutingBackplaneRecord:
    return SignalRoutingBackplaneRecord(
        backplane_id=f"bp_{uuid.uuid4()}",
        backplane_family=family,
        health_status="healthy"
    )

def add_backplane_channel(backplane: SignalRoutingBackplaneRecord, source_ref: str, target_ref: str) -> BackplaneChannelRecord:
    channel = BackplaneChannelRecord(
        backplane_channel_id=f"ch_{uuid.uuid4()}",
        source_segment_ref=source_ref,
        target_segment_ref=target_ref,
        backpressure_state="none",
        freshness_state="current",
        caveat_transfer_policy="strict",
        channel_status="active"
    )
    backplane.channel_refs.append(channel.backplane_channel_id)
    return channel

def apply_backpressure_to_flow(flow_ref: str, current_backpressure: str) -> str:
    if current_backpressure in ["high", "critical"]:
        return "flowed_degraded"
    return "flowed_bounded"

def summarize_backplane_health(backplane: SignalRoutingBackplaneRecord) -> dict:
    return {
        "id": backplane.backplane_id,
        "health": backplane.health_status,
        "channel_count": len(backplane.channel_refs)
    }
