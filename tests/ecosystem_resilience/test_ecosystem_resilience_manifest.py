from sports_signal_bot.ecosystem_resilience.contracts import MeshRoutingManifestRecord

def test_ecosystem_resilience_manifest():
    manifest = MeshRoutingManifestRecord(manifest_id="m1", mesh_refs=["mesh1", "mesh2"])
    assert manifest.manifest_id == "m1"
    assert len(manifest.mesh_refs) == 2
