from typing import Dict, Any, List
from .contracts import EcosystemSyncRunRecord, CatalogOverlayRecord, EcosystemRoutingRecord

class EcosystemSyncReporter:
    """Generates reports and KPI hooks for the sync process."""

    def generate_kpis(self, run: EcosystemSyncRunRecord, overlays: List[CatalogOverlayRecord], routing_decisions: List[EcosystemRoutingRecord]) -> Dict[str, Any]:
        """Generates key performance indicators."""
        active_subs = len(run.lag_records) # Rough proxy
        return {
            "active_subscription_count": active_subs,
            "sync_success_rate": 1.0 if run.status == "success" else 0.0,
            "sync_lag_score": sum(r.lag_seconds for r in run.lag_records) / max(1, len(run.lag_records)),
            "overlay_rebuild_frequency": len(overlays),
            "reroute_required_rate": sum(1 for d in routing_decisions if d.routing_status.value == "reroute_required") / max(1, len(routing_decisions)),
            "quarantined_subscription_rate": 0.0, # Placeholder
            "continuous_sync_health_index": 0.95 # Placeholder
        }

    def generate_report_sections(self, run: EcosystemSyncRunRecord) -> Dict[str, Any]:
        """Generates textual report sections."""
        return {
            "subscription_and_sync_health": f"Run {run.run_id} completed with status {run.status}.",
            "ecosystem_freshness_and_trust_summary": f"Tracked {len(run.lag_records)} lag records."
        }
