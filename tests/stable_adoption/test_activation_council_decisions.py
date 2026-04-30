import pytest
from sports_signal_bot.stable_adoption.council import build_activation_council_packet
from sports_signal_bot.stable_adoption.contracts import ActivationDecisionType

def test_activation_council_decision_approve():
    packet = build_activation_council_packet(
        adoption_id="adp_01",
        blockers=[],
        evidence_complete=True,
        scope="narrow_family",
        allowed_scopes=["narrow_family"],
        rollback_ready=True,
        verification_plan_complete=True
    )
    assert ActivationDecisionType.APPROVE_ACTIVATION.value in packet.recommendations

def test_activation_council_decision_reject_safety():
    from sports_signal_bot.stable_adoption.contracts import AdoptionBlockerRecord
    import datetime
    blocker = AdoptionBlockerRecord(
        blocker_id="blk_01",
        adoption_id="adp_01",
        blocker_family="test",
        severity="critical",
        reversibility="hard",
        description="Critical error"
    )
    packet = build_activation_council_packet(
        adoption_id="adp_01",
        blockers=[blocker],
        evidence_complete=True,
        scope="narrow_family",
        allowed_scopes=["narrow_family"],
        rollback_ready=True,
        verification_plan_complete=True
    )
    assert ActivationDecisionType.REJECT_ACTIVATION.value in packet.recommendations
