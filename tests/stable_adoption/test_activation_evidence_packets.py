import pytest
from sports_signal_bot.stable_adoption.evidence import build_activation_evidence_packet
from sports_signal_bot.stable_adoption.contracts import ActivationDecisionType

def test_evidence_packet_creation():
    packet = build_activation_evidence_packet("adp_01", ActivationDecisionType.APPROVE_ACTIVATION, "council_01", [], ["ev_01"])
    assert packet.approval_status == "approved"
    assert packet.decision_type == ActivationDecisionType.APPROVE_ACTIVATION
