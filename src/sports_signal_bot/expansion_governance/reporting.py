from typing import Dict, Any
from .contracts import ExpansionGovernanceManifest

def extract_kpi_hooks(manifest: ExpansionGovernanceManifest) -> Dict[str, Any]:
    """Extracts KPI metrics for reporting dashboards."""
    summary = manifest.control_tower_summary

    return {
        "expansion_budget_utilization": sum(summary.budget_usage_summary.values()) / max(len(summary.budget_usage_summary), 1),
        "global_pressure_index": summary.global_pressure_band,
        "family_freeze_rate": len(summary.family_freezes),
        "active_wave_count": summary.active_waves,
        "active_cohort_count": summary.active_cohorts
    }
