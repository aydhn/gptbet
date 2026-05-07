from typing import Dict, Any

def generate_supermesh_hardening_manifest(
    supermesh_summary: dict,
    fabric_summary: dict,
    pulse_summary: dict,
    observatory_summary: dict,
    matrix_summary: dict,
    budget_summary: dict
) -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "pack_name": "post-100-pack-16",
        "supermesh_summary": supermesh_summary,
        "fabric_summary": fabric_summary,
        "pulse_summary": pulse_summary,
        "observatory_summary": observatory_summary,
        "matrix_summary": matrix_summary,
        "budget_summary": budget_summary,
        "overall_readiness": "ready" if (
            supermesh_summary.get("status") != "supermesh_blocked" and
            fabric_summary.get("status") != "fabric_blocked" and
            pulse_summary.get("status") != "lane_blocked" and
            observatory_summary.get("status") != "observatory_blocked" and
            budget_summary.get("blockers", 0) == 0
        ) else "blocked"
    }
