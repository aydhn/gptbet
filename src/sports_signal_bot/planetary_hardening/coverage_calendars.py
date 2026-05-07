import uuid
from typing import List, Optional
from src.sports_signal_bot.planetary_hardening.contracts import (
    PlanetaryCoverageCalendarRecord,
    CoverageCalendarZoneRecord,
    CoverageCalendarWindowRecord,
    CoverageCalendarOwnerRecord,
    CoverageCalendarSeamRecord,
    CoverageCalendarGapRecord,
    CoverageCalendarReachabilityRecord,
    CoverageCalendarResidueRecord,
    PlanetaryCoverageCalendarWarningRecord
)

def build_planetary_coverage_calendar(calendar_family: str, zone_refs: List[CoverageCalendarZoneRecord]) -> PlanetaryCoverageCalendarRecord:
    return PlanetaryCoverageCalendarRecord(
        planetary_coverage_calendar_id=f"pcc_{uuid.uuid4().hex[:8]}",
        calendar_family=calendar_family,
        zone_refs=zone_refs,
        calendar_status="calendar_review_only"
    )

def add_calendar_window(calendar: PlanetaryCoverageCalendarRecord, window: CoverageCalendarWindowRecord) -> PlanetaryCoverageCalendarRecord:
    calendar.window_refs.append(window)
    return calendar

def verify_planetary_coverage_calendar(calendar: PlanetaryCoverageCalendarRecord, reject_stale: bool = True) -> PlanetaryCoverageCalendarRecord:
    warnings = []
    has_gap = len(calendar.gap_refs) > 0
    has_unreachable = any(not r.is_reachable for r in calendar.reachability_refs)
    has_missing_ack = any(not r.is_acknowledged for r in calendar.reachability_refs)
    has_stale_window = any(w.is_stale for w in calendar.window_refs)

    if has_gap:
        warnings.append(PlanetaryCoverageCalendarWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Calendar has gaps."))

    if has_unreachable or has_missing_ack:
        warnings.append(PlanetaryCoverageCalendarWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Reachability issues detected."))
        calendar.calendar_status = "calendar_caveated" if has_missing_ack and not has_unreachable else "calendar_gapped"

    if has_stale_window:
        warnings.append(PlanetaryCoverageCalendarWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Stale window detected."))
        if reject_stale:
            calendar.calendar_status = "calendar_caveated"

    if not calendar.owner_refs:
        calendar.calendar_status = "calendar_gapped"
        warnings.append(PlanetaryCoverageCalendarWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Ownerless calendar."))

    if not warnings and calendar.owner_refs and not has_gap:
        calendar.calendar_status = "calendar_verified"

    calendar.warnings.extend(warnings)
    return calendar

def detect_planetary_calendar_gaps(calendar: PlanetaryCoverageCalendarRecord) -> List[CoverageCalendarGapRecord]:
    # Simplified gap detection
    gaps = []
    if len(calendar.window_refs) == 0:
        gaps.append(CoverageCalendarGapRecord(gap_id=f"gap_{uuid.uuid4().hex[:8]}", description="No windows defined in calendar"))
    return gaps

def summarize_planetary_coverage_calendar(calendar: PlanetaryCoverageCalendarRecord) -> dict:
    return {
        "id": calendar.planetary_coverage_calendar_id,
        "family": calendar.calendar_family,
        "status": calendar.calendar_status,
        "warnings": [w.message for w in calendar.warnings],
        "windows_count": len(calendar.window_refs),
        "gaps_count": len(calendar.gap_refs)
    }
