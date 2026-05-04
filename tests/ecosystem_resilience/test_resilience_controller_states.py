from sports_signal_bot.ecosystem_resilience.controllers import build_ecosystem_resilience_controller, evaluate_controller_signals, trigger_controller_decision

def test_resilience_controller_states():
    controller = build_ecosystem_resilience_controller("c1", "federation_health", [], [])
    eval_res = evaluate_controller_signals(controller, "critical", 0)
    controller = trigger_controller_decision(controller, eval_res)

    assert controller.current_state == "degraded_state"
