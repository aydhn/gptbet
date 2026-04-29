import pytest
from sports_signal_bot.schema_governance.manifests import StandardManifest

def test_manifest_envelope_standardization():
    manifest = StandardManifest(
        manifest_family="test_family",
        schema_version="v1.0.0",
        producer_component="test_producer",
        artifact_family="test_artifact",
        artifact_id="123",
        run_id="run123",
        payload={"data": "value"}
    )
    assert manifest.manifest_family == "test_family"
    assert manifest.payload["data"] == "value"
