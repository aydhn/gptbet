from typing import List
from .contracts import SchedulerCadenceFabricRecord, CadenceFabricLaneRecord

def build_scheduler_cadence_fabric(fabric_id: str, family: str) -> SchedulerCadenceFabricRecord:
    return SchedulerCadenceFabricRecord(
        scheduler_cadence_fabric_id=fabric_id,
        fabric_family=family,
        fabric_status="fabric_verified"
    )

def add_cadence_fabric_lane(fabric: SchedulerCadenceFabricRecord, lane: CadenceFabricLaneRecord):
    fabric.lane_refs.append(lane.lane_id)
    if lane.is_ownerless and lane.is_critical:
        fabric.fabric_status = "fabric_gapped"

def verify_scheduler_cadence_fabric(fabric: SchedulerCadenceFabricRecord) -> str:
    return fabric.fabric_status

def summarize_scheduler_cadence_fabric(fabric: SchedulerCadenceFabricRecord) -> dict:
    return {
        "id": fabric.scheduler_cadence_fabric_id,
        "family": fabric.fabric_family,
        "status": fabric.fabric_status,
        "lane_count": len(fabric.lane_refs),
        "packet_count": len(fabric.packet_refs)
    }
