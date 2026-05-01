import pytest
from sports_signal_bot.external_audit_exchange.triage import compute_triage_priority, incorporate_reputation_into_triage
from sports_signal_bot.external_audit_exchange.routing import route_challenge_packet
from sports_signal_bot.external_audit_exchange.contracts import ChallengeExchangePacketRecord, ChallengeTriageRecord

def test_compute_triage_priority():
    packet = ChallengeExchangePacketRecord(
        packet_id="1", challenge_ref="c1", severity="critical", target_ref="t1", safe_payload={}
    )
    assert compute_triage_priority(packet) == "high"

def test_incorporate_reputation_into_triage():
    triage = ChallengeTriageRecord(triage_id="t1", challenge_ref="c1", status="open", priority="high", assigned_responder_class="expert")
    updated_triage = incorporate_reputation_into_triage(triage, 20.0)
    assert updated_triage.assigned_responder_class == "internal_review"

def test_route_challenge_packet():
    packet = ChallengeExchangePacketRecord(
        packet_id="1", challenge_ref="c1", severity="critical", target_ref="t1", safe_payload={}
    )
    routing = route_challenge_packet(packet, 90.0)
    assert routing.suggested_responder_class == "expert"
    assert routing.priority_score == 90.0
