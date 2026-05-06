from src.sports_signal_bot.geo_quorum_hardening.operator_coverage import build_global_operator_coverage_synthesis

def test_build_global_operator_coverage_synthesis_healthy():
    inputs = {
        "ownerless_critical_window": False,
        "escalation_unreachable": False,
        "stale_calendar_data": False
    }
    record = build_global_operator_coverage_synthesis(inputs)
    assert record.synthesis_status == "coverage_synthesized"

def test_build_global_operator_coverage_synthesis_blocked():
    inputs = {
        "ownerless_critical_window": True,
        "escalation_unreachable": False,
        "stale_calendar_data": False
    }
    record = build_global_operator_coverage_synthesis(inputs)
    assert record.synthesis_status == "coverage_blocked"
