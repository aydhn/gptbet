"""
Safety contract validation logic.
"""
from typing import Dict, Any, List
from .contracts import SafetyValidationRunRecord, SafetyViolationRecord

def build_safety_contracts() -> Dict[str, Any]:
    return {"contracts_loaded": True}

def validate_safety_invariants(module: str, state: Dict[str, Any]) -> SafetyValidationRunRecord:
    violations = []
    if not state.get("no_safe_visibility", True):
        violations.append(SafetyViolationRecord(
            invariant_id="no_safe_visibility_preserved",
            severity="high",
            context={"module": module},
            details="no_safe_visibility omitted."
        ))
    if not state.get("sovereignty_preserved", True):
         violations.append(SafetyViolationRecord(
            invariant_id="sovereignty_precedence",
            severity="critical",
            context={"module": module},
            details="Sovereignty masking detected."
        ))
    status = "healthy" if not violations else "violated"
    return SafetyValidationRunRecord(
        validation_run_id=f"val_{module}",
        target_module=module,
        checked_invariants=["no_safe_visibility_preserved", "sovereignty_precedence"],
        violations=violations,
        status=status
    )

def classify_safety_violation(violation: SafetyViolationRecord) -> str:
    return violation.severity

def summarize_safety_validation(runs: List[SafetyValidationRunRecord]) -> Dict[str, Any]:
    total_violations = sum(len(r.violations) for r in runs)
    critical_violations = sum(1 for r in runs for v in r.violations if v.severity == "critical")
    return {
        "total_runs": len(runs),
        "total_violations": total_violations,
        "critical_violations": critical_violations,
        "status": "release_ready" if critical_violations == 0 else "blocked"
    }
