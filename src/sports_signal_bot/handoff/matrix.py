import uuid
from typing import Dict, Any, List
from .contracts import ReadinessBand

def build_readiness_matrix(candidate_context: Dict[str, Any]) -> Dict[str, Any]:
    matrix = {}

    # 1. Simulation
    sim_score = candidate_context.get("simulation_score", 0.0)
    matrix["simulation"] = {
        "score": sim_score,
        "band": ReadinessBand.PASS if sim_score >= 0.9 else (ReadinessBand.WARN if sim_score >= 0.7 else ReadinessBand.FAIL),
        "notes": "Strong simulation results." if sim_score >= 0.9 else "Simulation needs improvement."
    }

    # 2. Gates
    gates_clean = candidate_context.get("gates_clean", False)
    matrix["gates"] = {
        "band": ReadinessBand.PASS if gates_clean else ReadinessBand.FAIL,
        "notes": "All gates passed." if gates_clean else "Gate failures detected."
    }

    # 3. Approvals
    approvals_complete = candidate_context.get("approvals_complete", False)
    matrix["approvals"] = {
        "band": ReadinessBand.PASS if approvals_complete else ReadinessBand.WARN,
        "notes": "Approvals complete." if approvals_complete else "Pending final approvals."
    }

    # 4. Evidence
    evidence_score = candidate_context.get("evidence_score", 0.0)
    matrix["evidence"] = {
        "score": evidence_score,
        "band": ReadinessBand.PASS if evidence_score >= 0.85 else (ReadinessBand.WARN if evidence_score >= 0.6 else ReadinessBand.FAIL),
        "notes": "Solid evidence backing." if evidence_score >= 0.85 else "Weak evidence."
    }

    # 5. Stability
    stability_score = candidate_context.get("stability_score", 0.0)
    matrix["stability"] = {
        "score": stability_score,
        "band": ReadinessBand.PASS if stability_score >= 0.95 else ReadinessBand.WARN,
        "notes": "Stable across channels." if stability_score >= 0.95 else "Some instability noted."
    }

    # 6. Rollback Readiness
    rollback_ready = candidate_context.get("rollback_ready", False)
    matrix["rollback_readiness"] = {
         "band": ReadinessBand.PASS if rollback_ready else ReadinessBand.FAIL,
         "notes": "Rollback procedure defined." if rollback_ready else "Rollback procedure missing."
    }

    return matrix

def validate_matrix_completeness(matrix: Dict[str, Any]) -> bool:
    required_dimensions = ["simulation", "gates", "approvals", "evidence", "stability", "rollback_readiness"]
    return all(dim in matrix for dim in required_dimensions)

def classify_readiness_outcome(matrix: Dict[str, Any]) -> ReadinessBand:
    fails = sum(1 for dim in matrix.values() if dim["band"] == ReadinessBand.FAIL)
    warns = sum(1 for dim in matrix.values() if dim["band"] == ReadinessBand.WARN)

    if fails > 0:
        return ReadinessBand.FAIL
    elif warns > 2:
        return ReadinessBand.WARN
    else:
        return ReadinessBand.PASS
