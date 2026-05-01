from sports_signal_bot.verifier_portal.packets import build_profile_specific_packet

def test_build_profile_specific_packet():
    data = {"test": "data", "signer_metadata": {"signer_id": "test"}}

    packet_public = build_profile_specific_packet("public_viewer", "publication_index_view", data)
    assert packet_public.audience_profile == "public_viewer"
    assert packet_public.redaction_profile == "full"

    packet_auditor = build_profile_specific_packet("external_auditor", "publication_index_view", data)
    assert packet_auditor.audience_profile == "external_auditor"
    assert packet_auditor.redaction_profile == "none"
