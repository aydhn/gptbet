from sports_signal_bot.handoff.blockers import detect_kill_before_handoff_conditions
from sports_signal_bot.handoff.contracts import HandoffKillReason

def test_detect_kill_before_handoff_conditions():
    context = {"is_stale": True}
    assert detect_kill_before_handoff_conditions("h1", context) == HandoffKillReason.STALE_CANDIDATE_PACKAGE

def test_detect_kill_before_handoff_conditions_safe():
    context = {"is_stale": False, "critical_blocker_count": 0, "rollback_notes_complete": True}
    assert detect_kill_before_handoff_conditions("h1", context) == HandoffKillReason.NOT_KILLED
