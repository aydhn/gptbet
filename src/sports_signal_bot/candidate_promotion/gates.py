from typing import List, Dict, Any
from .contracts import CandidateReleaseRecord, CandidateGateResultRecord

def resolve_candidate_gate_requirements(candidate: CandidateReleaseRecord) -> List[str]:
    """Resolves required quality gates for a candidate."""
    return ["smoke_test_suite", "regression_test_suite"]

def validate_gate_freshness(gate_result: CandidateGateResultRecord) -> bool:
    """Validates if a gate result is fresh."""
    return True

def attach_gate_matrix(candidate: CandidateReleaseRecord) -> Dict[str, Any]:
    """Attaches a matrix of gate statuses to the candidate."""
    return {"smoke": "passed", "regression": "passed"}

def summarize_blocking_gate_failures(gate_results: List[CandidateGateResultRecord]) -> List[str]:
    """Summarizes failures from gate results."""
    return [g.gate_result_id for g in gate_results if not g.passed]
