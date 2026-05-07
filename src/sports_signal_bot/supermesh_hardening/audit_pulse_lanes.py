from typing import List
from .contracts import GlobalAuditPulseLaneRecord, AuditPulseRecord

def build_global_audit_pulse_lane(lane_id: str, family: str) -> GlobalAuditPulseLaneRecord:
    return GlobalAuditPulseLaneRecord(
        global_audit_pulse_lane_id=lane_id,
        lane_family=family,
        lane_status="lane_verified"
    )

def emit_audit_pulse(lane: GlobalAuditPulseLaneRecord, pulse: AuditPulseRecord):
    lane.pulse_refs.append(pulse.pulse_id)
    if pulse.is_stale:
        lane.lane_status = "lane_caveated"

def summarize_global_audit_pulse_lane(lane: GlobalAuditPulseLaneRecord) -> dict:
    return {
        "id": lane.global_audit_pulse_lane_id,
        "family": lane.lane_family,
        "status": lane.lane_status,
        "pulse_count": len(lane.pulse_refs),
        "delivery_count": len(lane.delivery_refs),
        "miss_count": len(lane.miss_refs)
    }
