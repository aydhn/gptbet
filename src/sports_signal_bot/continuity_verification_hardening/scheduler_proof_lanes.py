from typing import List, Dict, Any
from .contracts import (
    SchedulerProofLaneRecord,
    SchedulerProofLaneFamily,
    SchedulerProofLaneStatus,
    SchedulerProofPacketRecord
)

def build_scheduler_proof_lane(lane_id: str, family: SchedulerProofLaneFamily) -> SchedulerProofLaneRecord:
    return SchedulerProofLaneRecord(
        scheduler_proof_lane_id=lane_id,
        lane_family=family,
        lane_status=SchedulerProofLaneStatus.lane_gapped
    )

def build_scheduler_proof_packet(packet_id: str, is_stale: bool = False) -> SchedulerProofPacketRecord:
    return SchedulerProofPacketRecord(
        packet_id=packet_id,
        is_stale=is_stale
    )

def verify_scheduler_proof_lane(lane: SchedulerProofLaneRecord, packets: List[SchedulerProofPacketRecord]) -> SchedulerProofLaneRecord:
    if not packets:
        lane.lane_status = SchedulerProofLaneStatus.lane_gapped
        return lane

    has_stale = any(p.is_stale for p in packets)
    has_caveats = len(lane.warnings) > 0

    if has_stale:
        lane.lane_status = SchedulerProofLaneStatus.lane_review_only
    elif has_caveats:
        lane.lane_status = SchedulerProofLaneStatus.lane_caveated
    else:
        lane.lane_status = SchedulerProofLaneStatus.lane_verified

    return lane

def replay_scheduler_proof_lane(lane: SchedulerProofLaneRecord) -> Dict[str, Any]:
    return {
        "lane_id": lane.scheduler_proof_lane_id,
        "replay_successful": True,
        "status": lane.lane_status
    }

def summarize_scheduler_proof_lane(lane: SchedulerProofLaneRecord) -> Dict[str, Any]:
    return {
        "id": lane.scheduler_proof_lane_id,
        "status": lane.lane_status,
        "packets": len(lane.packet_refs),
        "residues": len(lane.residue_refs)
    }
