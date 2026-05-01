from typing import Dict, Any, List
from .contracts import ExternalAuditManifest
import datetime
import uuid

def generate_external_audit_manifest(stats: Dict[str, Any]) -> ExternalAuditManifest:
    return ExternalAuditManifest(
        manifest_id=str(uuid.uuid4()),
        exported_requests=stats.get("exported", 0),
        imported_responses=stats.get("imported", 0),
        quarantined_responses=stats.get("quarantined", 0),
        notarizations_verified=stats.get("notarizations_verified", 0),
        notarizations_unverified=stats.get("notarizations_unverified", 0),
        reputation_distribution=stats.get("reputation_distribution", {})
    )
