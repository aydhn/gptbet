import pytest
from sports_signal_bot.external_audit_exchange.packets import build_safe_exchange_packet

def test_build_safe_exchange_packet():
    payload = {"some_data": 123, "sensitive_data": "secret"}
    packet = build_safe_exchange_packet("target_1", payload, profile="strict")
    assert packet.safe_payload.get("sensitive_data") == "[REDACTED]"
    assert packet.target_ref == "target_1"

def test_build_safe_exchange_packet_with_proofs():
    payload = {"some_data": 123, "sensitive_data": "secret"}
    proofs = ["proof1", "proof2"]
    packet = build_safe_exchange_packet("target_1", payload, profile="strict", proofs=proofs)
    assert packet.safe_payload.get("sensitive_data") == "[REDACTED]"
    assert packet.safe_payload.get("proofs") == proofs
