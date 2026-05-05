import pytest
from sports_signal_bot.concurrency_hardening.race_probes import build_race_probe_run, perturb_execution_schedule, detect_race_signals

def test_perturb_execution_schedule():
    ops = ["a", "b", "c", "d"]
    reversed_ops = perturb_execution_schedule(ops, seed=42, strategy="reverse")
    assert reversed_ops == ["d", "c", "b", "a"]

def test_detect_race_signals():
    run = build_race_probe_run("simultaneous_read_write_probe", 42, "interleave")
    violation = detect_race_signals(run, "expected", "actual")
    assert violation is not None
    assert run.run_status == "race_detected"
    assert run.violations_detected == 1
