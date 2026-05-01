from sports_signal_bot.verifier_portal.consistency import validate_portal_freshness, attach_freshness_warnings, detect_stale_public_packets, block_misleading_current_labels
from sports_signal_bot.verifier_portal.contracts import VerificationViewPacketRecord

def test_freshness_validation():
    packet = VerificationViewPacketRecord(
        packet_id="p1", packet_family="test", audience_profile="public_viewer", view_name="test",
        redaction_profile="full", freshness="current", supersession_status="active"
    )
    assert validate_portal_freshness(packet)

    packet.freshness = "stale"
    assert not validate_portal_freshness(packet)

def test_attach_freshness_warnings():
    packet = VerificationViewPacketRecord(
        packet_id="p1", packet_family="test", audience_profile="public_viewer", view_name="test",
        redaction_profile="full", freshness="stale", supersession_status="active"
    )
    packet = attach_freshness_warnings(packet)
    assert len(packet.warnings) == 1
    assert "not current" in packet.warnings[0]

def test_block_misleading_labels():
    packet = VerificationViewPacketRecord(
        packet_id="p1", packet_family="test", audience_profile="public_viewer", view_name="test",
        redaction_profile="full", freshness="current", supersession_status="active"
    )
    packet = block_misleading_current_labels(packet, "stale")
    assert packet.freshness == "stale"
    assert len(packet.warnings) == 1
