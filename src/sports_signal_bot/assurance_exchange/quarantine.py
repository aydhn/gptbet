from typing import List, Dict, Any
from .contracts import AssuranceQuarantineRecord

def quarantine_assurance_packet(
    quarantine_id: str,
    packet_id: str,
    reason: str
) -> AssuranceQuarantineRecord:
    """Places an assurance packet in quarantine."""
    return AssuranceQuarantineRecord(
        quarantine_id=quarantine_id,
        packet_id=packet_id,
        reason=reason,
        status="active"
    )

def decide_quarantine_release(quarantine: AssuranceQuarantineRecord, release_conditions_met: bool) -> bool:
    """Decides if an item can be released from quarantine."""
    if release_conditions_met:
        quarantine.status = "released"
        return True
    return False

def summarize_quarantine_pressure(quarantines: List[AssuranceQuarantineRecord]) -> Dict[str, Any]:
    active = sum(1 for q in quarantines if q.status == "active")
    return {
        "total_quarantined": len(quarantines),
        "active_quarantines": active
    }

def escalate_quarantine_if_critical(quarantine: AssuranceQuarantineRecord) -> None:
    if "critical" in quarantine.reason.lower():
        quarantine.status = "escalated"
