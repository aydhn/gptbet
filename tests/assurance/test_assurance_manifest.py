import pytest
from sports_signal_bot.assurance.manifests import generate_assurance_manifest

def test_assurance_manifest():
    man = generate_assurance_manifest({"test": "ok"})
    assert "manifest_id" in man
