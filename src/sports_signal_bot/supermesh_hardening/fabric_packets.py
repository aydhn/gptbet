from typing import List
from .contracts import CadenceFabricPacketRecord, CadenceFabricLaneRecord, SchedulerCadenceFabricRecord

def build_cadence_fabric_packet(packet_id: str, lane_ref: str, is_stale: bool = False) -> CadenceFabricPacketRecord:
    return CadenceFabricPacketRecord(
        packet_id=packet_id,
        lane_ref=lane_ref,
        is_stale=is_stale
    )

def verify_cadence_fabric_lane(lane: CadenceFabricLaneRecord) -> bool:
    if lane.is_critical and lane.is_ownerless:
        return False
    return True

def compute_cadence_fabric_lag(fabric: SchedulerCadenceFabricRecord) -> float:
    # Placeholder for computing overall lag based on drift refs
    return 0.0

def detect_cadence_fabric_gaps(lanes: List[CadenceFabricLaneRecord], packets: List[CadenceFabricPacketRecord]) -> List[str]:
    gaps = []
    for lane in lanes:
        if lane.is_critical and lane.is_ownerless:
            gaps.append(f"Gap: Ownerless critical lane {lane.lane_id}")
    for packet in packets:
        if packet.is_stale:
            gaps.append(f"Gap: Stale packet {packet.packet_id}")
    return gaps

def summarize_cadence_fabric_lanes(lanes: List[CadenceFabricLaneRecord]) -> dict:
    return {
        "total_lanes": len(lanes),
        "critical_lanes": sum(1 for lane in lanes if lane.is_critical),
        "ownerless_lanes": sum(1 for lane in lanes if lane.is_ownerless)
    }
