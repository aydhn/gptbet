import pytest
from sports_signal_bot.ecosystem_sync.manifests import build_overlay_manifest, emit_sync_artifacts
from sports_signal_bot.ecosystem_sync.contracts import EcosystemSyncRunRecord
from datetime import datetime

def test_emit_artifacts():
    run = EcosystemSyncRunRecord(
        run_id="run_1",
        plan_id="plan_1",
        status="success",
        start_time=datetime.utcnow()
    )

    audit = emit_sync_artifacts(run, {"summary": "test"})
    assert audit.run_ref == "run_1"
    assert audit.summary == {"summary": "test"}

def test_build_manifest():
    manifest = build_overlay_manifest([])
    assert manifest.overlays == []
    assert manifest.manifest_id.startswith("mani_")
