import pytest
from sports_signal_bot.geo_hardening.operator_calendars import build_operator_calendar_audit, verify_calendar_coverage
from sports_signal_bot.geo_hardening.calendar_handoffs import verify_calendar_handoff, validate_escalation_reachability, detect_ownerless_windows

def test_multi_region_operator_calendar_gap_set():
    # Multi-region operator calendar gap set
    shift_1 = {"id": "1", "start_time": 0, "end_time": 100, "owner": "alice"}
    shift_2 = {"id": "2", "start_time": 100, "end_time": 200, "owner": "bob"}
    shift_3 = {"id": "3", "start_time": 200, "end_time": 300, "owner": None}

    assert verify_calendar_handoff(shift_1, shift_2) is True
    assert verify_calendar_handoff(shift_2, shift_3) is False # no owner

    calendar = {"owners": ["alice", "bob"]}
    assert validate_escalation_reachability(calendar, ["alice", "bob"]) is True
    assert validate_escalation_reachability(calendar, ["alice", "charlie"]) is False

    gaps = detect_ownerless_windows([shift_1, shift_2, shift_3])
    assert gaps == ["3"]
