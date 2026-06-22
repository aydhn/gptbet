from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class SupermeshManifestInputs:
    supermesh_summary: dict
    fabric_summary: dict
    pulse_summary: dict
    observatory_summary: dict
    matrix_summary: dict
    budget_summary: dict

def generate_supermesh_hardening_manifest(
    inputs: SupermeshManifestInputs
) -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "pack_name": "post-100-pack-16",
        "supermesh_summary": inputs.supermesh_summary,
        "fabric_summary": inputs.fabric_summary,
        "pulse_summary": inputs.pulse_summary,
        "observatory_summary": inputs.observatory_summary,
        "matrix_summary": inputs.matrix_summary,
        "budget_summary": inputs.budget_summary,
        "overall_readiness": "ready" if (
            inputs.supermesh_summary.get("status") != "supermesh_blocked" and
            inputs.fabric_summary.get("status") != "fabric_blocked" and
            inputs.pulse_summary.get("status") != "lane_blocked" and
            inputs.observatory_summary.get("status") != "observatory_blocked" and
            inputs.budget_summary.get("blockers", 0) == 0
        ) else "blocked"
    }
