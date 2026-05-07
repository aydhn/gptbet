import uuid
from typing import List
from src.sports_signal_bot.planetary_hardening.contracts import (
    CalendarShiftRecord,
    CalendarHandoffRecord,
    CalendarAckRecord,
    CalendarContinuityRecord,
    CalendarMismatchRecord,
    CalendarLagRecord,
    CalendarHealthMarkerRecord,
    CoverageCalendarSeamRecord
)

def verify_calendar_handoff(handoff: CalendarHandoffRecord, ack: CalendarAckRecord) -> CalendarHealthMarkerRecord:
    status = "healthy" if ack.is_acknowledged else "unacknowledged"
    return CalendarHealthMarkerRecord(marker_id=f"marker_{uuid.uuid4().hex[:8]}", status=status)

def validate_calendar_reachability(owner: str, is_reachable: bool) -> CalendarHealthMarkerRecord:
    status = "reachable" if is_reachable else "unreachable"
    return CalendarHealthMarkerRecord(marker_id=f"marker_{uuid.uuid4().hex[:8]}", status=status)

def detect_calendar_seams(shifts: List[CalendarShiftRecord]) -> List[CoverageCalendarSeamRecord]:
    seams = []
    if len(shifts) > 1:
        for i in range(len(shifts) - 1):
            seams.append(CoverageCalendarSeamRecord(seam_id=f"seam_{uuid.uuid4().hex[:8]}", is_gapped=False))
    return seams

def summarize_calendar_windows(windows: List[dict]) -> dict:
    return {
        "total_windows": len(windows)
    }
