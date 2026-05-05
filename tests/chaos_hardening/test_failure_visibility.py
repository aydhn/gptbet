import pytest
from sports_signal_bot.chaos_hardening.contracts import FailureVisibilityRecord

def test_failure_visibility():
    visibility = FailureVisibilityRecord(visibility_id="vis-1", surfaces=[], warnings=[])
    assert visibility.visibility_id == "vis-1"
