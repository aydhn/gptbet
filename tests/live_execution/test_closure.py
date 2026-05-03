from sports_signal_bot.live_execution.closure import start_closure_verification_session, verify_runtime_closure
from sports_signal_bot.live_execution.contracts import CompletionClass

def test_closure_verification():
    closure = start_closure_verification_session("lane_1", ["signal_A", "signal_B"])
    res1 = verify_runtime_closure(closure, ["signal_A"])
    assert res1 == CompletionClass.NOT_VERIFIED

    res2 = verify_runtime_closure(closure, ["signal_A", "signal_B"])
    assert res2 == CompletionClass.VERIFIED
