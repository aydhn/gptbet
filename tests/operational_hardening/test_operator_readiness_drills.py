from sports_signal_bot.operational_hardening.drills import build_operator_readiness_drill

def test_build_operator_readiness_drill():
    drill = build_operator_readiness_drill("degraded_output_operator_drill", ["scenario-1"])
    assert drill.drill_family == "degraded_output_operator_drill"
    assert drill.readiness_status == "readiness_verified"
