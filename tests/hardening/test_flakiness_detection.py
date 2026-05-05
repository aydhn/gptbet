import pytest
from sports_signal_bot.hardening.flakiness import run_flakiness_probe

def test_run_flakiness_probe():
    case = run_flakiness_probe("cmd", 5)
    assert not case.inconsistent_outputs
    assert case.run_count == 5
