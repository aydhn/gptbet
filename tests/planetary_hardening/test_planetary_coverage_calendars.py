import pytest
from src.sports_signal_bot.planetary_hardening.coverage_calendars import (
    build_planetary_coverage_calendar,
    add_calendar_window,
    verify_planetary_coverage_calendar
)
from src.sports_signal_bot.planetary_hardening.contracts import (
    CoverageCalendarZoneRecord,
    CoverageCalendarWindowRecord,
    CoverageCalendarOwnerRecord
)

def test_build_planetary_coverage_calendar():
    cal = build_planetary_coverage_calendar("test_family", [CoverageCalendarZoneRecord(zone_id="z1", owner="o1")])
    assert cal.calendar_family == "test_family"
    assert len(cal.zone_refs) == 1
    assert cal.calendar_status == "calendar_review_only"

def test_verify_planetary_coverage_calendar_no_owner():
    cal = build_planetary_coverage_calendar("test_family", [CoverageCalendarZoneRecord(zone_id="z1", owner="o1")])
    cal = verify_planetary_coverage_calendar(cal)
    assert cal.calendar_status == "calendar_gapped"
    assert len(cal.warnings) == 1

def test_verify_planetary_coverage_calendar_with_owner_and_stale():
    cal = build_planetary_coverage_calendar("test_family", [CoverageCalendarZoneRecord(zone_id="z1", owner="o1")])
    cal.owner_refs.append(CoverageCalendarOwnerRecord(owner_id="o1", contact="c1"))
    add_calendar_window(cal, CoverageCalendarWindowRecord(window_id="w1", family="f1", is_stale=True))
    cal = verify_planetary_coverage_calendar(cal, reject_stale=True)
    assert cal.calendar_status == "calendar_caveated"
    assert len(cal.warnings) == 1
