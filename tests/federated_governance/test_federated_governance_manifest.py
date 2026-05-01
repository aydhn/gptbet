from sports_signal_bot.federated_governance.manifests import write_federated_manifest
from sports_signal_bot.federated_governance.contracts import FederatedManifest
import tempfile
import os

def test_write_manifest():
    manifest = FederatedManifest(
        manifest_id="man1",
        planes=[],
        active_escalations=[],
        budget_summary={},
        mesh_hotspots=[],
        suspensions=[],
        overrides=[]
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        path = write_federated_manifest(manifest, output_dir=tmpdir)
        assert os.path.exists(path)
        with open(path, 'r') as f:
            content = f.read()
            assert "man1" in content
