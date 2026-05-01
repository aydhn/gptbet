from datetime import datetime
from src.sports_signal_bot.public_verification_gateway.contracts import DisclosureBundleRecord
from src.sports_signal_bot.public_verification_gateway.profiles import get_default_profiles
from src.sports_signal_bot.public_verification_gateway.packets import build_public_packet

def test_build_public_packet():
    profile = get_default_profiles()[0] # public_minimal
    bundle = DisclosureBundleRecord(
        disclosure_bundle_id="b1",
        bundle_family="policy_bundle_disclosure",
        publication_profile="public_minimal",
        source_refs=[],
        included_items=[],
        redaction_profile="strict",
        verification_refs=["proof1"],
        publishability_status="publish_ready",
        created_at=datetime.utcnow()
    )
    packet = build_public_packet(bundle, {"data": "safe"}, profile)
    assert packet.packet_id == "pkt_pub_b1"
    assert not packet.challenge_instructions # Minimal has no challenge intake allowed
