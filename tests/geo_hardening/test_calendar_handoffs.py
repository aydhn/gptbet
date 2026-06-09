import pytest
from sports_signal_bot.geo_hardening.calendar_handoffs import verify_calendar_handoff

def test_verify_calendar_handoff_valid():
    shift_from = {"end_time": "12:00", "owner": "alice"}
    shift_to = {"start_time": "12:00", "owner": "bob"}
    assert verify_calendar_handoff(shift_from, shift_to) is True

def test_verify_calendar_handoff_mismatched_times():
    shift_from = {"end_time": "12:00", "owner": "alice"}
    shift_to = {"start_time": "12:30", "owner": "bob"}
    assert verify_calendar_handoff(shift_from, shift_to) is False

def test_verify_calendar_handoff_missing_owner():
    shift_from = {"end_time": "12:00", "owner": "alice"}
    shift_to = {"start_time": "12:00", "owner": ""}
    assert verify_calendar_handoff(shift_from, shift_to) is False

    shift_to2 = {"start_time": "12:00"}
    assert verify_calendar_handoff(shift_from, shift_to2) is False
