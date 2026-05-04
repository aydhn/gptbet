import pytest
from sports_signal_bot.governance_assurance.manifests import create_governance_assurance_manifest

def test_create_manifest():
    manifest = create_governance_assurance_manifest("man1", ["d1", "d2"])
    assert manifest.manifest_id == "man1"
    assert len(manifest.dashboard_refs) == 2
    assert "T" in manifest.timestamp
