from datetime import datetime, timezone
from sports_signal_bot.governance_assurance.contracts import GovernanceAssuranceDashboardManifestRecord

def create_governance_assurance_manifest(manifest_id: str, dashboard_refs: list[str]) -> GovernanceAssuranceDashboardManifestRecord:
    return GovernanceAssuranceDashboardManifestRecord(
        manifest_id=manifest_id,
        dashboard_refs=dashboard_refs,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
