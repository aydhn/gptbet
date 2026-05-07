from .base import GlobalHardeningStrategy
from typing import Dict, Any

class ConservativeGlobalHardeningStrategy(GlobalHardeningStrategy):
    def evaluate_quorum_mesh(self, mesh_data: Dict[str, Any]) -> Dict[str, Any]:
        # reject any stale nodes immediately
        warnings = mesh_data.get("warnings", [])
        status = "mesh_verified"
        if warnings:
            status = "mesh_blocked"
        return {"status": status, "release_blocking": status == "mesh_blocked"}

    def evaluate_planetary_coverage(self, coverage_data: Dict[str, Any]) -> Dict[str, Any]:
        warnings = coverage_data.get("warnings", [])
        status = "coverage_verified"
        if warnings:
            status = "coverage_blocked"
        return {"status": status, "release_blocking": status == "coverage_blocked"}

    def evaluate_continuity_drill(self, drill_data: Dict[str, Any]) -> Dict[str, Any]:
        warnings = drill_data.get("warnings", [])
        residue = drill_data.get("residue", [])
        status = "continuity_rehearsed_honestly"
        if warnings or residue:
            status = "continuity_blocked"
        return {"status": status, "release_blocking": status == "continuity_blocked"}

    def evaluate_recovery_governance(self, gov_data: Dict[str, Any]) -> Dict[str, Any]:
        warnings = gov_data.get("warnings", [])
        status = "governance_verified"
        if warnings:
            status = "governance_blocked"
        return {"status": status, "release_blocking": status == "governance_blocked"}
