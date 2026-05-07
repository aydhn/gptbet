from typing import List
from .contracts import (
    SchedulerBusRecord, BusFamily, BusStatus,
    SchedulerBusLaneRecord, SchedulerBusPacketRecord, SchedulerBusCadenceRecord,
    SchedulerBusHealthRecord, SchedulerBusWarningRecord
)

def build_scheduler_bus(bus_id: str, family: BusFamily) -> SchedulerBusRecord:
    return SchedulerBusRecord(scheduler_bus_id=bus_id, bus_family=family)

def add_scheduler_bus_lane(bus: SchedulerBusRecord, lane: SchedulerBusLaneRecord) -> None:
    bus.lane_refs.append(lane)

def build_scheduler_bus_packet(packet_id: str) -> SchedulerBusPacketRecord:
    return SchedulerBusPacketRecord(packet_id=packet_id)

def verify_scheduler_bus(bus: SchedulerBusRecord) -> SchedulerBusHealthRecord:
    stale_packets = [p for p in bus.packet_refs if p.is_stale]
    missing_acks = [p for p in bus.packet_refs if not p.has_ack]
    ownerless_lanes = [l for l in bus.lane_refs if l.is_ownerless]
    drifts = [c for c in bus.cadence_refs if c.drift_ms > 0]

    if ownerless_lanes or missing_acks:
        bus.bus_status = BusStatus.BUS_BLOCKED
        bus.warnings.append(SchedulerBusWarningRecord(warning_id="blocked_bus", description="Ownerless lanes or missing acks"))
        return SchedulerBusHealthRecord(is_healthy=False, status=BusStatus.BUS_BLOCKED)

    if stale_packets or drifts:
        bus.bus_status = BusStatus.BUS_CAVEATED
        bus.warnings.append(SchedulerBusWarningRecord(warning_id="caveated_bus", description="Stale packets or drift present"))
        return SchedulerBusHealthRecord(is_healthy=False, status=BusStatus.BUS_CAVEATED)

    if not bus.lane_refs:
        bus.bus_status = BusStatus.BUS_GAPPED
        return SchedulerBusHealthRecord(is_healthy=False, status=BusStatus.BUS_GAPPED)

    bus.bus_status = BusStatus.BUS_VERIFIED
    return SchedulerBusHealthRecord(is_healthy=True, status=BusStatus.BUS_VERIFIED)

def summarize_scheduler_bus(bus: SchedulerBusRecord) -> dict:
    return {
        "id": bus.scheduler_bus_id,
        "family": bus.bus_family.value,
        "status": bus.bus_status.value,
        "warnings_count": len(bus.warnings)
    }

def verify_scheduler_bus_lane(lane: SchedulerBusLaneRecord) -> bool:
    return not lane.is_ownerless

def compute_scheduler_bus_lag(bus: SchedulerBusRecord) -> int:
    return sum(c.drift_ms for c in bus.cadence_refs)

def detect_scheduler_bus_gaps(bus: SchedulerBusRecord) -> List[str]:
    gaps = []
    if not bus.lane_refs:
        gaps.append("missing_lanes")
    if not bus.packet_refs:
        gaps.append("missing_packets")
    return gaps

def summarize_scheduler_bus_lanes(lanes: List[SchedulerBusLaneRecord]) -> dict:
    return {
        "total": len(lanes),
        "ownerless": sum(1 for l in lanes if l.is_ownerless)
    }
