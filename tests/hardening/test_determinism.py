import pytest
from sports_signal_bot.hardening.determinism import build_determinism_run, compare_determinism_runs

def test_determinism_run_creation():
    run = build_determinism_run(
        "run_1", "test_family", "cmd_1", {"k": "v"}, {"in": "data"}, {"env": "prod"}, "seed_42", "clock_1", {"out": "hash1"}
    )
    assert run.determinism_run_id == "run_1"
    assert run.parity_status == "parity_matched"

def test_compare_determinism_runs():
    run1 = build_determinism_run("r1", "f", "c", {}, {}, {}, "s", "c", {"o": "h1"})
    run2 = build_determinism_run("r2", "f", "c", {}, {}, {}, "s", "c", {"o": "h2"})
    status = compare_determinism_runs(run1, run2)
    assert status == "parity_mismatched"
