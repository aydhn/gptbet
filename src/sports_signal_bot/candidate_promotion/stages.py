from typing import List, Dict, Any, Tuple
from .contracts import (
    CandidateReleaseRecord,
    CandidateValidationStageRecord,
    StageCheckRecord
)

def build_candidate_validation_plan(candidate: CandidateReleaseRecord) -> List[str]:
    """Builds a validation plan with stages for a candidate based on family and risk."""
    stages = [
        "integrity_validation",
        "safety_validation",
        "simulation_validation"
    ]
    if candidate.risk_level in ["high", "critical"]:
        stages.append("review_readiness_validation")
    stages.append("quality_gates_validation")
    stages.append("release_readiness_validation")
    return stages

def run_candidate_stage_validation(candidate: CandidateReleaseRecord, stage_name: str) -> CandidateValidationStageRecord:
    """Runs a single validation stage for a candidate."""
    checks = [StageCheckRecord(check_id="c1", description="Baseline check", passed=True)]
    passed = True

    # Simple logic for simulation safety failure
    if stage_name == "safety_validation" and candidate.risk_level == "critical":
        passed = False
        checks.append(StageCheckRecord(check_id="c2", description="Safety boundary check", passed=False))

    return CandidateValidationStageRecord(
        validation_id=f"val_{stage_name}",
        candidate_id=candidate.candidate_release_id,
        stage_id=stage_name,
        passed=passed,
        checks=checks
    )

def summarize_stage_results(results: List[CandidateValidationStageRecord]) -> Dict[str, Any]:
    """Summarizes stage results."""
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    return {"total": len(results), "passed": passed, "failed": failed}

def detect_blocking_stage_failures(results: List[CandidateValidationStageRecord]) -> List[str]:
    """Returns a list of failed stage IDs."""
    return [r.stage_id for r in results if not r.passed]

def explain_stage_outcome(result: CandidateValidationStageRecord) -> str:
    """Explains why a stage passed or failed."""
    if result.passed:
        return f"Stage {result.stage_id} passed cleanly."
    return f"Stage {result.stage_id} failed due to checks: {[c.description for c in result.checks if not c.passed]}"
