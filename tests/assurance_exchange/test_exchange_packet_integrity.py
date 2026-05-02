from sports_signal_bot.assurance_exchange.packets import build_exchange_packet, verify_exchange_packet_integrity
from datetime import datetime, timedelta

def test_verify_exchange_packet_integrity():
    packet = build_exchange_packet(
        exchange_packet_id="pkt_1",
        packet_family="test",
        source_registry_ref="local",
        carried_bundle_refs=["b1"],
        claim_refs=["c1"],
        attestation_refs=[],
        proof_refs=[]
    )
    assert verify_exchange_packet_integrity(packet) is True

def test_verify_exchange_packet_integrity_expired():
    packet = build_exchange_packet(
        exchange_packet_id="pkt_1",
        packet_family="test",
        source_registry_ref="local",
        carried_bundle_refs=["b1"],
        claim_refs=["c1"],
        attestation_refs=[],
        proof_refs=[],
        valid_until=datetime.utcnow() - timedelta(days=1)
    )
    assert verify_exchange_packet_integrity(packet) is False
