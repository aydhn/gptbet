from sports_signal_bot.endurance_hardening.soak import build_soak_endurance_run

def test_build_soak_endurance_run():
    run = build_soak_endurance_run("test_1", "mixed_surface_soak")
    assert run.soak_run_id == "test_1"
    assert run.run_family == "mixed_surface_soak"
    assert run.outcome_status == "endurance_blocked"
