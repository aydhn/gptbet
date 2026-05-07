from typing import List
from .contracts import AuditPulseDeliveryRecord, AuditPulseMissRecord, GlobalAuditPulseLaneRecord

def verify_audit_pulse_delivery(delivery: AuditPulseDeliveryRecord) -> bool:
    return delivery.has_ack

def verify_pulse_handoff(lane: GlobalAuditPulseLaneRecord, delivery: AuditPulseDeliveryRecord) -> bool:
    if not delivery.has_ack:
        lane.lane_status = "lane_gapped"
        return False
    return True

def validate_pulse_reachability(lane: GlobalAuditPulseLaneRecord) -> bool:
    # Placeholder
    return True

def detect_audit_pulse_gaps(lane: GlobalAuditPulseLaneRecord, deliveries: List[AuditPulseDeliveryRecord], misses: List[AuditPulseMissRecord]) -> List[str]:
    gaps = []
    for miss in misses:
        if miss.is_hidden:
            gaps.append(f"Gap: Hidden pulse miss {miss.miss_id}")
        else:
            gaps.append(f"Gap: Pulse miss {miss.miss_id}")
    for delivery in deliveries:
        if not delivery.has_ack:
            gaps.append(f"Gap: Delivery without ack {delivery.delivery_id}")
    return gaps

def detect_pulse_misses(misses: List[AuditPulseMissRecord]) -> List[str]:
    return [m.miss_id for m in misses]

def summarize_pulse_delivery(deliveries: List[AuditPulseDeliveryRecord], misses: List[AuditPulseMissRecord]) -> dict:
    return {
        "total_deliveries": len(deliveries),
        "acked_deliveries": sum(1 for d in deliveries if d.has_ack),
        "total_misses": len(misses),
        "hidden_misses": sum(1 for m in misses if m.is_hidden)
    }
