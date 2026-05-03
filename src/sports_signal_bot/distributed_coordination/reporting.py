import json
from typing import Dict, Any

class DistributedReportingManager:
    """Manages reporting output for the distributed coordination fabric."""

    def generate_kpi_summary(self,
                             admission_rate: float,
                             divergence_rate: float,
                             failover_success: float,
                             snapshot_freshness: float) -> Dict[str, Any]:
        """Generates a dictionary of distributed KPIs."""
        return {
            "cluster_schedule_admission_rate": admission_rate,
            "broker_pool_divergence_rate": divergence_rate,
            "failover_revalidation_success_rate": failover_success,
            "cluster_snapshot_freshness_score": snapshot_freshness,
        }

    def write_summary_report(self, path: str, data: Dict[str, Any]) -> None:
        """Writes the summary report to a JSON file."""
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
