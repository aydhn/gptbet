from sports_signal_bot.remediation_lanes.closure import verify_loop_closure
from sports_signal_bot.remediation_lanes.contracts import LoopClosureRecord, LoopClosureOutcome

def test_closure_verification():
    record = LoopClosureRecord(closure_id="c1", lane_ref="l1", outcome=LoopClosureOutcome.closed_clean)
    assert verify_loop_closure(record) == True
