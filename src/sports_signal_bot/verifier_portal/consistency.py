from typing import Dict, Any, List
from .contracts import VerificationViewPacketRecord, DashboardFeedRecord

def validate_portal_freshness(packet: VerificationViewPacketRecord) -> bool:
    return packet.freshness == "current"

def validate_feed_consistency(feed: DashboardFeedRecord) -> bool:
    return feed.freshness == "fresh"

def detect_stale_public_packets(packets: List[VerificationViewPacketRecord]) -> List[VerificationViewPacketRecord]:
    return [p for p in packets if p.freshness != "current"]

def attach_freshness_warnings(packet: VerificationViewPacketRecord) -> VerificationViewPacketRecord:
    if packet.freshness != "current":
        packet.warnings.append("Warning: This packet is not current.")
    return packet

def block_misleading_current_labels(packet: VerificationViewPacketRecord, actual_status: str) -> VerificationViewPacketRecord:
    if packet.freshness == "current" and actual_status != "current":
        packet.freshness = actual_status
        packet.warnings.append("Warning: Freshness label corrected.")
    return packet
