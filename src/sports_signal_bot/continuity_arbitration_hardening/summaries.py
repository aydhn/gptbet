from typing import Dict, Any

def generate_overall_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    rail_caveated = sum(1 for r in report.get("continuity_arbitration_rails", []) if r["status"] != "rail_verified")
    fabric_caveated = sum(1 for r in report.get("scheduler_recovery_fabrics", []) if r["status"] != "fabric_verified")
    mesh_broken = sum(1 for r in report.get("archive_proof_meshes", []) if r["status"] != "mesh_verified")
    ledger_caveated = sum(1 for r in report.get("worldwide_visibility_ledgers", []) if r["status"] != "ledger_verified")

    return {
        "rail_caveated_counts": rail_caveated,
        "fabric_caveated_counts": fabric_caveated,
        "mesh_broken_counts": mesh_broken,
        "ledger_caveated_counts": ledger_caveated,
        "overall_status": "caveated" if any([rail_caveated, fabric_caveated, mesh_broken, ledger_caveated]) else "verified"
    }
