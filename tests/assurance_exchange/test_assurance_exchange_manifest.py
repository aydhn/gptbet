from sports_signal_bot.assurance_exchange.manifests import build_assurance_exchange_manifest

def test_build_assurance_exchange_manifest():
    m = build_assurance_exchange_manifest("m_1")
    assert m.manifest_id == "m_1"
