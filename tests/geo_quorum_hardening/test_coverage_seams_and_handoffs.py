from src.sports_signal_bot.geo_quorum_hardening.coverage_seams import verify_coverage_handoff

def test_verify_coverage_handoff():
    assert verify_coverage_handoff({"ack_present": True}) == "verified"
    assert verify_coverage_handoff({"ack_present": False}) == "caveated"
