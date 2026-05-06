from src.sports_signal_bot.geo_quorum_hardening.passive_checkpoints import verify_failback_readiness

def test_verify_failback_readiness():
    assert verify_failback_readiness({"readiness_measured": True}) == "ready"
    assert verify_failback_readiness({"readiness_measured": False}) == "not_ready"
