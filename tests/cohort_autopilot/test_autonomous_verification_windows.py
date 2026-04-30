from datetime import datetime
from sports_signal_bot.cohort_autopilot.verification import build_verification_windows, run_window_verification
from sports_signal_bot.cohort_autopilot.contracts import VerificationSignalRecord, WindowOutcome

def test_verification_windows():
    now = datetime.utcnow()
    windows = build_verification_windows("c1", now)
    assert len(windows) == 2

    signals = [VerificationSignalRecord(signal_id="s1", cohort_id="c1", signal_type="error_rate", is_positive=True)]
    outcome = run_window_verification(windows[0], signals)
    assert outcome.outcome == WindowOutcome.VERIFIED_CLEAN
