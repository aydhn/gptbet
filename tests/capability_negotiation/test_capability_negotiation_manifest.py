from sports_signal_bot.capability_negotiation.contracts import RegistryCapabilityManifest

def test_manifest_creation():
    manifest = RegistryCapabilityManifest(
        manifest_id="test",
        profiles=[],
        negotiations=[],
        portable_bundles=[],
        notarizations=[],
        drifts=[],
        onboardings=[],
        summary={"status": "ok"}
    )
    assert manifest.manifest_id == "test"
    assert manifest.summary["status"] == "ok"
