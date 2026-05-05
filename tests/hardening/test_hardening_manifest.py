import pytest
from sports_signal_bot.hardening.contracts import HardeningManifestRecord
from sports_signal_bot.hardening.manifests import serialize_manifest

def test_serialize_manifest():
    manifest = HardeningManifestRecord(
        manifest_id="m1", timestamp="t1", determinism_runs=[], regression_cases=[],
        safety_validations=[], replay_parity_runs=[], artifact_reproducibility=[],
        flakiness_cases=[], release_blockers=[], overall_health="healthy"
    )
    res = serialize_manifest(manifest)
    assert "m1" in res
