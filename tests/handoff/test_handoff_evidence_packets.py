from sports_signal_bot.handoff.evidences import build_handoff_evidence_packet

def test_build_handoff_evidence_packet():
    context = {"evidence_score": 0.9, "approvals_complete": True}
    packet = build_handoff_evidence_packet("h1", context, "d1")
    assert "strong_evidence" in packet.explanations
    assert "governance" in packet.explanations
