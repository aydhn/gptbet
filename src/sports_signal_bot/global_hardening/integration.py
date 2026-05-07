import json
from .contracts import (
    RegionalQuorumMeshRecord,
    PlanetaryCoverageSynthesisRecord,
    GlobalContinuityDrillRecord,
    CrossRegionRecoveryGovernanceRecord,
    GlobalResilienceBudgetsRecord
)
from .quorum_meshes import summarize_regional_quorum_mesh
from .planetary_coverage import summarize_planetary_coverage
from .continuity_drills import summarize_global_continuity_drill
from .recovery_governance import summarize_cross_region_governance
from .budgets import summarize_global_resilience_budgets

def build_global_continuity_matrix(
    meshes: list[RegionalQuorumMeshRecord],
    coverages: list[PlanetaryCoverageSynthesisRecord],
    drills: list[GlobalContinuityDrillRecord],
    govs: list[CrossRegionRecoveryGovernanceRecord],
    budgets: list[GlobalResilienceBudgetsRecord]
) -> dict:

    mesh_summaries = [summarize_regional_quorum_mesh(m) for m in meshes]
    cov_summaries = [summarize_planetary_coverage(c) for c in coverages]
    drill_summaries = [summarize_global_continuity_drill(d) for d in drills]
    gov_summaries = [summarize_cross_region_governance(g) for g in govs]
    budget_summaries = [summarize_global_resilience_budgets(b) for b in budgets]

    matrix = {
        "meshes": mesh_summaries,
        "coverages": cov_summaries,
        "drills": drill_summaries,
        "governance": gov_summaries,
        "budgets": budget_summaries
    }

    return matrix

def summarize_global_continuity_matrix(matrix: dict) -> dict:

    mesh_verified = sum(1 for m in matrix["meshes"] if m["status"] == "mesh_verified")
    cov_verified = sum(1 for c in matrix["coverages"] if c["status"] == "coverage_verified")
    drill_honest = sum(1 for d in matrix["drills"] if d["status"] == "continuity_rehearsed_honestly")
    gov_verified = sum(1 for g in matrix["governance"] if g["status"] == "governance_verified")

    total_warnings = sum(m.get("warnings", 0) for m in matrix["meshes"]) + \
                     sum(c.get("warnings", 0) for c in matrix["coverages"]) + \
                     sum(d.get("warnings", 0) for d in matrix["drills"]) + \
                     sum(g.get("warnings", 0) for g in matrix["governance"]) + \
                     sum(b.get("warnings", 0) for b in matrix["budgets"])

    release_blocker_count = 0
    # Add simple release blocking logic if total_warnings > 0, maybe threshold
    if total_warnings > 0:
        release_blocker_count = 1

    return {
        "mesh_verified_count": mesh_verified,
        "coverage_verified_count": cov_verified,
        "drill_honest_count": drill_honest,
        "governance_verified_count": gov_verified,
        "total_warnings": total_warnings,
        "release_blockers": release_blocker_count,
        "overall_health": "verified" if release_blocker_count == 0 else "blocked"
    }

def export_artifacts(matrix: dict, summary: dict):
    with open("global_continuity_matrix.json", "w") as f:
        json.dump(matrix, f, indent=2)
    with open("global_hardening_health_report.json", "w") as f:
        json.dump(summary, f, indent=2)
