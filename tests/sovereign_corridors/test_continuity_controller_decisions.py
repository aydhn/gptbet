from sports_signal_bot.sovereign_corridors.controllers import start_continuity_controller_session, escalate_continuity_gap, finalize_continuity_controller_decision
from sports_signal_bot.sovereign_corridors.contracts import ContinuityGapRecord

def test_controller():
    ctrl = start_continuity_controller_session("c1")
    assert ctrl.decision_status == "monitoring"

    gap = ContinuityGapRecord(gap_id="g1", severity="high")
    ctrl = escalate_continuity_gap(ctrl, gap)
    assert ctrl.decision_status == "blocked"

    dec = finalize_continuity_controller_decision(ctrl)
    assert dec.outcome == "continuity_blocked"
