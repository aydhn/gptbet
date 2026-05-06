from sports_signal_bot.operational_hardening.escalation import build_escalation_ladder

def test_build_escalation_ladder():
    ladder = build_escalation_ladder("freshness_escalation_ladder")
    assert ladder.ladder_family == "freshness_escalation_ladder"
    assert ladder.ladder_status == "ladder_ready"
