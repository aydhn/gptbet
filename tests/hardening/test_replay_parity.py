import pytest
from sports_signal_bot.hardening.replay_parity import run_replay_parity

def test_run_replay_parity_matched():
    run = run_replay_parity("fix1", {"a": 1}, {"a": 1})
    assert run.parity_status == "matched"

def test_run_replay_parity_mismatched():
    run = run_replay_parity("fix1", {"a": 1}, {"a": 2})
    assert run.parity_status == "mismatched"
