from sports_signal_bot.endurance_hardening.manifests import generate_endurance_hardening_manifest

def test_generate_endurance_hardening_manifest():
    manifest = generate_endurance_hardening_manifest()
    assert manifest["manifest_version"] == "1.0"
