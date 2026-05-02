from datetime import datetime
from typing import List, Dict, Any
from .contracts import (
    CatalogOverlayManifest,
    CatalogOverlayRecord,
    EcosystemSyncAuditRecord,
    EcosystemSyncRunRecord
)

def build_overlay_manifest(overlays: List[CatalogOverlayRecord]) -> CatalogOverlayManifest:
    """Builds a manifest containing the state of all current overlays."""
    return CatalogOverlayManifest(
        manifest_id=f"mani_{datetime.utcnow().timestamp()}",
        overlays=overlays,
        timestamp=datetime.utcnow()
    )

def emit_sync_artifacts(run: EcosystemSyncRunRecord, summary: Dict[str, Any]) -> EcosystemSyncAuditRecord:
    """Emits audit artifacts summarizing a sync run."""
    return EcosystemSyncAuditRecord(
        audit_id=f"audit_{datetime.utcnow().timestamp()}",
        run_ref=run.run_id,
        summary=summary,
        timestamp=datetime.utcnow()
    )
