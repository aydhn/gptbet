from sports_signal_bot.registry_conformance.manifests import generate_registry_manifest


def test_manifest():
    manifest = generate_registry_manifest("r1", 10, 2)
    assert manifest.registry_ref == "r1"
    assert manifest.total_entries == 10
