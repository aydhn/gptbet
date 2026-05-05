import pytest
from sports_signal_bot.concurrency_hardening.timeouts import run_timeout_probe, run_cancellation_probe

def test_run_timeout_probe():
    probe1 = run_timeout_probe("t1", True)
    assert probe1.status == "timeout_simulated"
    assert len(probe1.warnings) == 1

    probe2 = run_timeout_probe("t2", False)
    assert probe2.status == "completed"

def test_run_cancellation_probe():
    probe = run_cancellation_probe("t1", True)
    assert probe.status == "cancellation_simulated"
    assert len(probe.warnings) == 1
