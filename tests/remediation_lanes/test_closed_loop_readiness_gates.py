from sports_signal_bot.remediation_lanes.readiness import build_closed_loop_readiness_gates, evaluate_closed_loop_readiness
def test_readiness_gates():
    gate = build_closed_loop_readiness_gates("g1", "l1", ["chk1"])
    assert evaluate_closed_loop_readiness(gate) == True
