from sports_signal_bot.endurance_hardening.drift import build_drift_detection_run

def test_build_drift_detection_run():
    run = build_drift_detection_run("drift_1")
    assert run.drift_run_id == "drift_1"
    assert run.status == "drift_blocked"
