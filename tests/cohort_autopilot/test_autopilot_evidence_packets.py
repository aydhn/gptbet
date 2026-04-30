from sports_signal_bot.cohort_autopilot.evidence import build_growth_evidence_packet

def test_evidence_packet():
    packet = build_growth_evidence_packet("c1", {"reason": "Clean windows"})
    assert packet.cohort_id == "c1"
    assert packet.payload["reason"] == "Clean windows"
