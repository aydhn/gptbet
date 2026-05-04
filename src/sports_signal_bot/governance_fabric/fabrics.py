import uuid
import datetime
from typing import List, Optional

from .contracts import (
    ConsortiumSignalFabricRecord, FabricSegmentRecord, FabricChannelRecord,
    FabricFlowRecord, FabricSignalPacketRecord, FabricPressureRecordV2
)

def build_signal_fabric(family: str) -> ConsortiumSignalFabricRecord:
    return ConsortiumSignalFabricRecord(
        signal_fabric_id=f"fabric_{uuid.uuid4().hex[:8]}",
        fabric_family=family,
        segment_refs=[],
        channel_refs=[],
        active_signal_packet_refs=[],
        suppression_refs=[],
        corroboration_refs=[],
        health_status="healthy",
        warnings=[]
    )

def add_fabric_segment(fabric: ConsortiumSignalFabricRecord, segment_family: str) -> FabricSegmentRecord:
    segment = FabricSegmentRecord(
        segment_id=f"seg_{uuid.uuid4().hex[:8]}",
        segment_family=segment_family,
        participating_layer_refs=["layer1"],
        participating_member_refs=["member1"],
        scope_constraints=[],
        freshness_policy_ref="default_freshness",
        suppression_policy_ref="default_suppression",
        segment_status="active",
        warnings=[]
    )
    fabric.segment_refs.append(segment.segment_id)
    return segment

def add_fabric_channel(fabric: ConsortiumSignalFabricRecord, source_ref: str, target_ref: str) -> FabricChannelRecord:
    channel = FabricChannelRecord(
        channel_id=f"chan_{uuid.uuid4().hex[:8]}",
        source_segment_ref=source_ref,
        target_segment_ref=target_ref,
        supported_signal_families=["all"],
        supported_scope_classes=["all"],
        pressure_state="low",
        freshness_state="fresh",
        channel_status="active",
        caveat_transfer_policy="strict",
        warnings=[]
    )
    fabric.channel_refs.append(channel.channel_id)
    return channel

def route_signal_through_fabric(fabric: ConsortiumSignalFabricRecord, signal_ref: str, channels: List[str], pressure: str) -> FabricFlowRecord:
    outcome = "flowed_bounded"
    suppressions = []

    if pressure in ["high", "critical", "suppress_noncritical_signal_paths"]:
        outcome = "flowed_suppressed"
        suppressions.append(f"Suppressed due to pressure: {pressure}")
        fabric.suppression_refs.append(f"sup_{uuid.uuid4().hex[:8]}")
        fabric.warnings.append("Fabric under pressure, suppressing signals")

    return FabricFlowRecord(
        flow_id=f"flow_{uuid.uuid4().hex[:8]}",
        input_signal_ref=signal_ref,
        traversed_channel_refs=channels,
        provenance_chain=[signal_ref],
        freshness_decay=0.0,
        corroboration_updates=[],
        suppression_events=suppressions,
        projected_targets=["target1"],
        final_signal_state=outcome
    )

def compute_fabric_pressure(fabric: ConsortiumSignalFabricRecord, stale_density: float, conflict_density: float) -> FabricPressureRecordV2:
    outcome = "low"
    if stale_density > 0.5 or conflict_density > 0.5:
        outcome = "high"
        fabric.health_status = "degraded"
    if stale_density > 0.8:
        outcome = "suppress_noncritical_signal_paths"

    return FabricPressureRecordV2(
        pressure_id=f"press_{uuid.uuid4().hex[:8]}",
        fabric_ref=fabric.signal_fabric_id,
        stale_signal_density=stale_density,
        duplicate_signal_burst=0.0,
        conflicting_cluster_density=conflict_density,
        degraded_channel_ratio=0.0,
        corroboration_backlog=0,
        suppression_burden=0.0,
        provenance_gap_ratio=0.0,
        controller_alert_density=0.0,
        pressure_outcome=outcome
    )

def summarize_signal_fabric(fabric: ConsortiumSignalFabricRecord) -> str:
    return f"Fabric {fabric.signal_fabric_id} ({fabric.fabric_family}): Segments={len(fabric.segment_refs)}, Health={fabric.health_status}"
