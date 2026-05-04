import pytest
from sports_signal_bot.overlay_mesh_governance.manifests import generate_overlay_mesh_governance_manifest

def test_generate_manifest():
    m = generate_overlay_mesh_governance_manifest()
    assert m["phase"] == 82
    assert m["status"] == "active"
