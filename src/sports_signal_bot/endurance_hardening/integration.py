from typing import Dict, Any
from .soak import build_soak_endurance_run
from .drift import build_drift_detection_run
from .archives import build_archive_snapshot
from .runbooks import build_runbook_record
from .summaries import generate_endurance_hardening_summary
from .manifests import generate_endurance_hardening_manifest

def run_endurance_hardening_pack() -> Dict[str, Any]:
    soak_run = build_soak_endurance_run("soak_1", "mixed_surface_soak")
    drift_run = build_drift_detection_run("drift_1")
    archive_snap = build_archive_snapshot("snap_1", "soak_archive_snapshot")
    runbook_rec = build_runbook_record("rb_1", "degraded_output_runbook")

    results = {
        "soak": soak_run.dict(),
        "drift": drift_run.dict(),
        "archive": archive_snap.dict(),
        "runbook": runbook_rec.dict()
    }

    summary = generate_endurance_hardening_summary(results)
    manifest = generate_endurance_hardening_manifest()

    return {
        "results": results,
        "summary": summary,
        "manifest": manifest
    }
