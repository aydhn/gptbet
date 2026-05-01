from typing import Dict, Any, List
from .contracts import ExternalAuditManifest

def calculate_external_audit_kpis(manifest: ExternalAuditManifest) -> Dict[str, float]:
    kpis = {}
    total_responses = manifest.imported_responses
    if total_responses > 0:
        kpis["quarantine_rate"] = manifest.quarantined_responses / total_responses
    else:
        kpis["quarantine_rate"] = 0.0

    total_notarizations = manifest.notarizations_verified + manifest.notarizations_unverified
    if total_notarizations > 0:
        kpis["notarization_success_rate"] = manifest.notarizations_verified / total_notarizations
    else:
        kpis["notarization_success_rate"] = 0.0

    return kpis
