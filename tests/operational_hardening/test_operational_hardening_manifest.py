from sports_signal_bot.operational_hardening.manifests import create_manifest

def test_operational_manifest():
    assert create_manifest() == {"manifest_version": "1.0"}
