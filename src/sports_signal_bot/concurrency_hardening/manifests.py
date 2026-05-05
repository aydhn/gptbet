import json
import datetime
from typing import Dict, Any

class ConcurrencyHardeningOverallHealthRecord:
    def __init__(self, is_healthy: bool, status_summary: str, blocker_count: int):
        self.is_healthy = is_healthy
        self.status_summary = status_summary
        self.blocker_count = blocker_count
        self.generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_overall_health_report(manifests: Dict[str, Any]) -> Dict[str, Any]:
    """Builds an overall health report combining all manifests."""
    blocker_count = 0
    all_healthy = True

    # Check regressions
    if "regressions" in manifests and not manifests["regressions"].health.is_healthy:
        all_healthy = False
        blocker_count += len([r for r in manifests["regressions"].regressions if any(w.severity == "release_blocking" for w in r.warnings)])

    # Check races
    if "race_probes" in manifests and not manifests["race_probes"].health.is_healthy:
         all_healthy = False
         blocker_count += sum(1 for r in manifests["race_probes"].runs if r.run_status == "race_detected")

    # Check other criticals... (simplified for now)

    summary = f"Concurrency Hardening check complete. Found {blocker_count} release blockers."

    return {
        "overall_health": {
            "is_healthy": all_healthy and blocker_count == 0,
            "status_summary": summary,
            "blocker_count": blocker_count,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    }
