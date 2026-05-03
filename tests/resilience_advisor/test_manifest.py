from sports_signal_bot.resilience_advisor.manifests import generate_resilience_advisor_manifest

def test_generate_manifest():
    manifest = generate_resilience_advisor_manifest([])
    assert manifest.manifest_id.startswith("manifest_")
